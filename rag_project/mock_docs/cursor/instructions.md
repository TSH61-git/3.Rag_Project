# Development Instructions

## Installation Guide

### Prerequisites
- Node.js 18+
- PostgreSQL 14+
- npm or yarn

### Setup Steps
1. Clone the repository
2. Install dependencies: `npm install`
3. Create `.env` file with database credentials
4. Run migrations: `npm run migrate`
5. Start development server: `npm run dev`

## Coding Standards

### React Components
- Use functional components with hooks
- Follow naming convention: PascalCase for components
- Keep components small and focused
- Use TypeScript for type safety

### API Endpoints
- RESTful conventions
- Use proper HTTP status codes
- Always validate input data
- Return consistent error format

### Database
- Use migrations for schema changes
- Never commit sensitive data
- Use prepared statements to prevent SQL injection

## Sensitive Areas

### Authentication Module
**Sensitivity**: HIGH
**Warning**: This module handles user credentials and tokens. Any changes must be reviewed by security team.
**Last Modified**: 2024-01-20

### Payment Processing
**Sensitivity**: CRITICAL
**Warning**: Do not modify payment logic without PCI compliance review
**Status**: Not yet implemented
