package zoho

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

// BulkReadModule submits a bulk read job for a specific module and returns the job ID
func BulkReadModule(module string, fields []string, since string) (string, error) {
	log.Printf("[Zoho] Starting bulk read for module %s", module)

	// Special handling for Users module which doesn't support bulk read
	if module == "Users" {
		log.Printf("[Zoho] Users module doesn't support bulk read, using regular API endpoint")
		users, err := FetchUsers()
		if err != nil {
			return "", fmt.Errorf("failed to fetch users: %w", err)
		}
		// Save users data directly
		if err := saveToFile("users.json", users); err != nil {
			return "", fmt.Errorf("failed to save users data: %w", err)
		}
		return "USERS_FETCHED", nil
	}

	// Step 1: Validate and prepare fields
	validator := NewFieldValidator(module)
	if err := validator.Initialize(); err != nil {
		return "", fmt.Errorf("failed to initialize field validator: %w", err)
	}

	validFields, skippedFields, err := validator.ValidateFields(fields)
	if err != nil {
		return "", fmt.Errorf("field validation failed: %w", err)
	}

	// Log any skipped fields
	if len(skippedFields) > 0 {
		log.Printf("[Zoho] Skipped fields for bulk read in %s: %v", module, skippedFields)
	}

	if len(validFields) == 0 {
		return "", fmt.Errorf("no valid fields found for module %s", module)
	}

	// Step 2: Construct the request body according to v7 API specs
	requestBody := map[string]interface{}{
		"callback": map[string]interface{}{
			"url": "",
			"method": "post",
		},
		"query": map[string]interface{}{
			"module": map[string]interface{}{
				"api_name": module,
			},
			"page": 1,
			"fields": validFields,
		},
	}

	// Add modified time criteria if since is provided
	if since != "" {
		requestBody["query"].(map[string]interface{})["criteria"] = fmt.Sprintf("(Last_Modified_Time:after:%s)", since)
	}

	// Step 3: Submit the bulk read job
	jsonBody, err := json.Marshal(requestBody)
	if err != nil {
		return "", fmt.Errorf("failed to marshal request body: %w", err)
	}

	log.Printf("[Zoho] Submitting bulk read job for %s with fields: %v", module, validFields)
	log.Printf("[Zoho] Request body: %s", string(jsonBody))
	
	resp, err := zohoRequest("POST", "/crm/bulk/v7/read", bytes.NewBuffer(jsonBody))
	if err != nil {
		return "", fmt.Errorf("failed to submit bulk read job: %w", err)
	}
	defer resp.Body.Close()

	// Step 4: Parse the response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response body: %w", err)
	}

	if resp.StatusCode != http.StatusCreated {
		return "", fmt.Errorf("bulk read job submission failed with status %d: %s", resp.StatusCode, string(body))
	}

	var result struct {
		Data []struct {
			Details struct {
				ID string `json:"id"`
			} `json:"details"`
		} `json:"data"`
	}

	if err := json.Unmarshal(body, &result); err != nil {
		return "", fmt.Errorf("failed to parse response: %w", err)
	}

	if len(result.Data) == 0 || result.Data[0].Details.ID == "" {
		return "", fmt.Errorf("no job ID in response")
	}

	jobID := result.Data[0].Details.ID
	log.Printf("[Zoho] Successfully submitted bulk read job for %s. Job ID: %s", module, jobID)
	return jobID, nil
} 