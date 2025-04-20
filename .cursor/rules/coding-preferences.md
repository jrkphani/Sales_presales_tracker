# Coding Preferences for Sales Dashboard

## General Principles
- Always prefer simple solutions over complex ones
- Avoid duplication of code whenever possible
- Check for other areas of the codebase that might already have similar functionality
- Write clean, maintainable code with proper comments

## Project Structure
- Keep React components in the src/components directory, organized by feature
- Use the following structure for components:
  - `/components/charts` - Reusable chart components
  - `/components/layout` - Layout-related components
  - `/components/dashboard` - Dashboard panels and sections
- All sample data should be kept in src/data/sampleData.js
- CSS styles should be modular and component-specific

## Technical Stack
- React 18+ with functional components and hooks
- Recharts for all data visualizations
- Use ES6+ features but maintain browser compatibility
- Prefer array methods (map, filter, reduce) over for loops

## Feature Implementation
- All visualizations should be interactive with tooltips
- Ensure drill-down capability for each chart
- Implement proper error handling for data loading
- Ensure responsive design that works on all screen sizes

## Performance Considerations
- Optimize renders with React.memo where appropriate
- Use proper key attributes for all mapped elements
- Be mindful of expensive operations in render functions
- Consider lazy loading for components not immediately visible

## Styling Guidelines
- Use functional CSS approach with minimal nesting
- Avoid inline styles except for dynamic values
- Use consistent color scheme throughout the application
- Ensure all UI elements have proper spacing and alignment

## Data Handling
- Format currency values consistently using Intl.NumberFormat
- Handle empty or null data gracefully
- Implement proper data transformations for chart components
- Ensure calculations are accurate and optimized

## Testing
- Write unit tests for utility functions
- Create component tests for critical functionality
- Test edge cases like empty data sets, large numbers

## Accessibility
- Ensure proper color contrast for text elements
- Add ARIA attributes where needed
- Make sure keyboard navigation works correctly
- Include alt text for any icons or images
