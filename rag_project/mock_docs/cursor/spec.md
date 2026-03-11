# System Specification - E-Commerce Platform

## Project Overview
Building a modern e-commerce platform with React frontend and Node.js backend.

## Technical Decisions

### Database Choice
**Decision Date**: 2024-01-15
**Decision**: PostgreSQL for relational data
**Reasoning**: Need ACID compliance for transactions, complex queries for product catalog

### Authentication
**Decision Date**: 2024-01-20
**Decision**: JWT-based authentication with refresh tokens
**Warning**: Do not modify the JWT verification hook without thorough testing - this is critical for security

## Design System

### Color Palette
- Primary Color: #2563eb (Blue)
- Secondary Color: #10b981 (Green)
- Accent Color: #f59e0b (Orange)

### Typography
- Headings: Inter Bold
- Body: Inter Regular
- Code: JetBrains Mono

## Internationalization

### Supported Languages
- Hebrew (RTL)
- English (LTR)
- Arabic (RTL)

### RTL Rules
**Rule**: All Hebrew and Arabic interfaces must use RTL layout
**Exception**: Code snippets and API paths remain LTR
**Scope**: UI components only

## Database Schema

### Recent Changes (2024-02-10)
- Added `discount_percentage` field to `products` table
- Removed `old_price` field (replaced by discount calculation)
- Added `wishlist` table with user_id and product_id

### Tables
- users
- products
- orders
- order_items
- categories
- reviews
- wishlist (new)
