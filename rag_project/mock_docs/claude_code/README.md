# E-Commerce Platform - Claude Code Documentation

## Architecture Overview

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **State Management**: Redux Toolkit
- **Styling**: Tailwind CSS
- **Routing**: React Router v6

### Backend Architecture
- **Framework**: Express.js
- **ORM**: Prisma
- **Validation**: Zod
- **API Documentation**: Swagger/OpenAPI

## Key Decisions

### State Management
**Date**: 2024-01-18
**Decision**: Redux Toolkit for global state
**Alternatives Considered**: Context API, Zustand
**Reasoning**: Need for complex state logic, time-travel debugging, middleware support

### Styling Approach
**Date**: 2024-01-12
**Decision**: Tailwind CSS with custom design tokens
**Reasoning**: Rapid development, consistent design system, small bundle size

## UI/UX Guidelines

### Responsive Design
- Mobile-first approach
- Breakpoints: 640px, 768px, 1024px, 1280px
- Test on real devices, not just browser DevTools

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader friendly
- Color contrast ratio minimum 4.5:1

### RTL Support
**Rule**: All text content in Hebrew/Arabic must render RTL
**Implementation**: Use `dir="rtl"` attribute, CSS logical properties
**Testing**: Test with actual Hebrew/Arabic content, not Lorem Ipsum

## Performance Optimization

### Frontend
- Code splitting by route
- Lazy load images
- Memoize expensive computations
- Virtual scrolling for long lists

### Backend
- Database query optimization
- Redis caching for frequently accessed data
- Rate limiting on API endpoints
- Compression middleware

## Security Considerations

### Critical Security Rules
1. **Never expose API keys in frontend code**
2. **Always sanitize user input**
3. **Use HTTPS in production**
4. **Implement CSRF protection**
5. **Set secure HTTP headers**

### Recent Security Update (2024-02-05)
Added rate limiting to login endpoint to prevent brute force attacks.
Configuration: 5 attempts per 15 minutes per IP.
