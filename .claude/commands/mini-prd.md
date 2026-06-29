# mini-prd Command

Create a mini PRD for $ARGUMENTS that includes goal, requirements, and acceptance criteria.
create file at .docs/year(YYYY)/month(MM)/day(DD)/{number-in-DD-folder(01)}-{Feature Spec}/{Feature Spec}-spec.md.
check real current date first.
only 1 file.
must follow the format specified in the example bellow. do not add any additional information.
max 8000 characters if the result exceeds 8000 characters, just it is.

# example: User Authentication Feature Spec

## User Authentication Feature Spec
### Goal
Implement secure user authentication with JWT tokens

### Requirements
- Email/password login
- Password hashing with bcrypt
- JWT token generation
- Protected route middleware
- Input validation and sanitization

### Acceptance Criteria
- [ ] User can register with email/password
- [ ] User can login and receive JWT token
- [ ] Protected routes verify JWT tokens
- [ ] Passwords are properly hashed
- [ ] Input validation prevents injection attacksCopy

### Implementation Approach

### end to end system flow
use ascii diagram to show the flow of the feature from start to finish.

### Files to Modify

### Technical Constraints

### Success Metrics

### Risk Mitigation

### Documentation Updates Required

### Summary of Changes

