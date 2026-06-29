---
name: agent-delegation-rules
description: Delegation rules and guidelines for specialized agents in the host mobile app project
---

# Agent Delegation Rules - MANDATORY

## 🎯 Agent Ecosystem Overview

The host mobile app project uses specialized agents for different domains. **ALWAYS delegate to the appropriate agent** for their area of expertise.

## 📋 Available Agents and Their Responsibilities

### 1. 🔧 android-gradle-debugger
**EXCLUSIVE OWNER** of all Gradle and build operations.

**Delegate for:**
- ANY Gradle command execution
- Build operations (debug/release/APK/bundle)
- Test execution (unit/UI/screenshot/integration)
- Code quality (lint/static analysis)
- Build debugging and optimization
- Dependency conflict resolution

### 2. 🎨 compose-design-system
**EXPERT** in Figma-to-Compose implementation and design systems.

**Delegate for:**
- Implementing Figma designs in Jetpack Compose
- Creating reusable UI components
- Design token implementation
- Theme and styling consistency
- Material3 component usage
- UI state management patterns

### 3. 🏗️ mobile-architect-advisor
**AUTHORITY** on architecture and best practices.

**Delegate for:**
- Architecture decisions and patterns
- Code review for SOLID principles
- Module structure guidance
- Clean architecture implementation
- Dependency graph optimization
- Refactoring strategies

### 4. 🚀 feature-orchestrator
**COORDINATOR** for end-to-end feature implementation.

**Delegate for:**
- Multi-module feature planning
- Cross-team coordination
- Feature workflow orchestration
- Integration point identification
- Feature flag implementation
- Release readiness assessment

### 5. 📊 mobile-data-domain-engineer
**SPECIALIST** in data layer and domain logic.

**Delegate for:**
- Repository pattern implementation
- Data source architecture
- Domain model design
- Use case implementation
- Data flow optimization
- State management strategies

### 6. 🔒 security-compliance-officer
**GUARDIAN** of security and banking compliance.

**Delegate for:**
- Regulatory / compliance requirements
- Security vulnerability assessment
- Encryption implementation
- Authentication/authorization flows
- Sensitive data handling
- Certificate pinning setup
- Security audit reports

### 7. 🧪 test-automation-engineer
**MASTER** of testing strategies and automation.

**Delegate for:**
- Test strategy development
- Test coverage improvement
- UI test implementation
- Unit test creation
- Test fixture management
- Flaky test debugging
- CI/CD test optimization

### 8. ⚡ performance-optimizer
**EXPERT** in app performance and optimization.

**Delegate for:**
- Performance profiling
- Memory leak detection
- APK size reduction
- Build time optimization
- Startup time improvement
- UI lag investigation
- Battery usage optimization

### 9. 🛡️ code-quality-guardian
**ENFORCER** of coding standards and quality.

**Delegate for:**
- Code style enforcement
- Lint rule configuration
- Documentation standards
- Code complexity analysis
- Technical debt assessment
- Code review automation
- Clean code principles

## 🔄 Delegation Protocol

### General Flow
```
1. IDENTIFY: Determine the domain of the task
2. DELEGATE: Send clear request to appropriate agent
3. WAIT: For agent's analysis and response
4. INTEGRATE: Incorporate results into your work
5. VERIFY: Ensure all requirements are met
```

### Multi-Agent Coordination

#### Feature Implementation Flow
```mermaid
Feature Request
    ├─> feature-orchestrator (coordination)
    ├─> mobile-architect-advisor (architecture)
    ├─> compose-design-system (UI)
    ├─> mobile-data-domain-engineer (data layer)
    ├─> test-automation-engineer (testing)
    ├─> android-gradle-debugger (build/run)
    └─> code-quality-guardian (standards)
```

#### Security-Critical Features
```mermaid
Security Feature
    ├─> security-compliance-officer (requirements)
    ├─> mobile-architect-advisor (secure architecture)
    ├─> feature-orchestrator (implementation)
    ├─> test-automation-engineer (security tests)
    └─> android-gradle-debugger (validation)
```

## 📝 Delegation Examples

### ✅ CORRECT Delegation Patterns

#### Example 1: New Login Screen
```markdown
User: "Implement new login screen from Figma design"

Main Agent delegates:
→ compose-design-system: "Implement Figma login design #123"
→ security-compliance-officer: "Validate authentication security"
→ test-automation-engineer: "Create login UI tests"
→ android-gradle-debugger: "Run full test suite"
```

#### Example 2: Performance Issue
```markdown
User: "App is slow on startup"

Main Agent delegates:
→ performance-optimizer: "Profile startup performance"
→ mobile-architect-advisor: "Review initialization architecture"
→ code-quality-guardian: "Check for code smells in Application class"
→ android-gradle-debugger: "Measure build impact"
```

#### Example 3: Banking Feature
```markdown
User: "Add fund transfer feature"

Main Agent delegates:
→ security-compliance-officer: "Define security requirements for fund transfer"
→ feature-orchestrator: "Plan fund transfer implementation"
→ mobile-data-domain-engineer: "Design transfer data models"
→ test-automation-engineer: "Create transfer test scenarios"
```

### ❌ WRONG - Direct Execution Without Delegation

```markdown
# NEVER DO THIS:
Main Agent: "I'll implement the UI directly"
Main Agent: "I'll run the tests myself"
Main Agent: "I'll fix the performance issue"

# ALWAYS DO THIS:
Main Agent: "Delegating UI implementation to compose-design-system"
Main Agent: "Delegating test execution to android-gradle-debugger"
Main Agent: "Delegating performance analysis to performance-optimizer"
```

## 🎯 Quick Reference Table

| Task Category | Primary Agent | Supporting Agents |
|--------------|---------------|-------------------|
| Gradle/Build | android-gradle-debugger | - |
| UI Implementation | compose-design-system | mobile-architect-advisor |
| Architecture | mobile-architect-advisor | feature-orchestrator |
| Data Layer | mobile-data-domain-engineer | mobile-architect-advisor |
| Security | security-compliance-officer | test-automation-engineer |
| Testing | test-automation-engineer | android-gradle-debugger |
| Performance | performance-optimizer | android-gradle-debugger |
| Code Quality | code-quality-guardian | mobile-architect-advisor |
| Feature Planning | feature-orchestrator | All relevant agents |

## 🚨 Critical Rules

### MUST ALWAYS:
1. **Delegate** to specialized agents for their domains
2. **Wait** for agent responses before proceeding
3. **Coordinate** multiple agents for complex tasks
4. **Document** delegation decisions in responses
5. **Respect** agent expertise boundaries

### MUST NEVER:
1. **Execute** Gradle commands directly (use android-gradle-debugger)
2. **Implement** security without security-compliance-officer
3. **Design** UI without compose-design-system for Figma work
4. **Optimize** without performance-optimizer analysis
5. **Skip** test-automation-engineer for test strategies

## 🔐 Compliance Enforcement

### Violation Examples:
- Running `./gradlew` directly → Must use android-gradle-debugger
- Implementing auth without security review → Must use security-compliance-officer
- Creating UI without design system → Must use compose-design-system
- Writing tests without strategy → Must use test-automation-engineer

### Consequences of Non-Delegation:
- Security vulnerabilities
- Inconsistent implementations
- Performance degradation
- Failed compliance audits
- Technical debt accumulation
- Poor test coverage

## 📊 Delegation Metrics

Track delegation success:
- ✅ Tasks delegated to appropriate agents
- ✅ Agent recommendations followed
- ✅ Multi-agent coordination achieved
- ✅ Build/test validation completed
- ✅ Security reviews conducted

## 🔄 Emergency Protocols

### Production Issues:
1. security-compliance-officer (if security-related)
2. performance-optimizer (if performance-related)
3. android-gradle-debugger (for immediate debugging)
4. feature-orchestrator (for coordination)

### Build Failures:
1. android-gradle-debugger (primary)
2. mobile-architect-advisor (if architectural)
3. code-quality-guardian (if quality-related)

---

**Remember**: Each agent is an expert in their domain. Leverage their expertise for optimal results. The success of the project depends on proper delegation and coordination!