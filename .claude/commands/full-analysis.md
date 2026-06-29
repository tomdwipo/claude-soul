# Complete Codebase Analysis

Perform comprehensive analysis of the entire codebase: $ARGUMENTS

## Phase 1: Project Foundation & Structure
### 1.1 Project Overview
# Get project basics
pwd
ls -la
find . -maxdepth 2 -type d | head -20
1.2 Technology Stack Discovery

Read package.json, requirements.txt, Gemfile, pom.xml, Cargo.toml, go.mod
Identify programming languages used
List all dependencies and their versions
Understand build tools and configuration

1.3 Project Structure Mapping

Map all major directories and their purposes
Identify configuration directories
Locate documentation, tests, and build files
Find entry points and main application files

Phase 2: Architecture & Design Analysis
2.1 System Architecture

Identify architectural patterns (MVC, microservices, layered, etc.)
Map component relationships and dependencies
Understand data flow and control flow
Identify system boundaries and interfaces

2.2 Code Organization

Analyze module structure and organization
Identify separation of concerns
Map business logic distribution
Understand code layering (presentation, business, data)

Phase 3: Deep Code Analysis
3.1 Core Functionality Inventory
bash# Find all main files by language
find . -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.rs" -o -name "*.php" | grep -v node_modules | grep -v vendor | wc -l
3.2 Critical Components Analysis

Models/Entities: Data structures and business objects
Controllers/Handlers: Request processing and routing
Services/Business Logic: Core application logic
Views/Templates: UI components and rendering
Utilities/Helpers: Shared functionality
Configuration: Environment and app settings

3.3 Integration Points

Database connections and ORM usage
External API integrations
Authentication and authorization systems
Caching mechanisms
Message queues and event systems

Phase 4: Code Quality & Patterns Analysis
4.1 Coding Conventions

Naming conventions (variables, functions, classes, files)
Code formatting and style patterns
Comment and documentation patterns
Import/export organization

4.2 Design Patterns Usage

Identify common design patterns used
Analyze abstraction levels
Review inheritance and composition usage
Examine error handling patterns

4.3 Testing Strategy
bash# Find test files
find . -name "*test*" -o -name "*spec*" | grep -v node_modules

Test coverage and strategies
Testing frameworks and tools
Mock and fixture usage
Integration vs unit test patterns

Phase 5: Development Ecosystem Analysis
5.1 Development Workflow

Build systems and scripts
Development vs production configurations
Environment variable usage
Deployment and CI/CD setup

5.2 Dependencies & Security

Direct and transitive dependencies
Version constraints and compatibility
Security vulnerability assessment
License compatibility

5.3 Performance & Monitoring

Performance optimization patterns
Logging and monitoring setup
Caching strategies
Database query patterns

Phase 6: Documentation & Knowledge Extraction
6.1 Available Documentation

README files and setup instructions
API documentation
Code comments and inline docs
Architecture decision records

6.2 Git History Analysis
bash# Recent activity
git log --oneline -20
git shortlog -sn | head -10

Recent changes and development activity
Contributor patterns
Change frequency by component
Historical decision context

Execution Strategy:

Start with foundation files: README, package.json, main configs
Map the structure: Use ls, find, and tree commands
Read systematically: Start with entry points, follow imports
Analyze by layer: Database → Business Logic → API → Frontend
Cross-reference: Understand how components interact
Document patterns: Note recurring structures and conventions

Comprehensive Output Format:
Executive Summary

Project type and primary purpose
Technology stack and architecture style
Scale and complexity assessment
Key strengths and potential concerns

Detailed Architecture Map
Project: [Name]
├── Frontend Layer: [Technologies, patterns, structure]
├── API/Backend Layer: [Routes, controllers, services]
├── Business Logic Layer: [Core functionality, domain models]
├── Data Layer: [Database, ORM, repositories]
├── Infrastructure: [Config, deployment, monitoring]
└── Testing: [Strategy, coverage, tools]
Component Inventory
ComponentPurposeFilesDependenciesNotesAuthenticationUser managementauth/JWT, bcryptUses session-based authAPI GatewayRequest routingroutes/ExpressRESTful designDatabaseData persistencemodels/PostgreSQLWell-normalized schema
Development Guide

Adding new features: Step-by-step process
Code conventions: What patterns to follow
Testing approach: How to write and run tests
Deployment process: How to build and deploy
Common gotchas: Things to watch out for

Recommendations

Code quality improvements
Architecture enhancements
Security considerations
Performance optimizations
Technical debt areas

Quality Checklist:

 Understand main user flows
 Know data models and relationships
 Identify all external dependencies
 Understand error handling approach
 Know testing and deployment process
 Recognize coding patterns and conventions
 Can explain architecture to someone else
 Identified potential improvement areas

