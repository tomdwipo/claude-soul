# Complete Mobile Codebase Analysis

Perform comprehensive mobile-focused analysis: $ARGUMENTS

## Phase 1: Mobile Platform & Technology Discovery
### 1.1 Platform Identification
```bash
# Detect mobile platform type
ls -la | grep -E "(android|ios|flutter|react-native|cordova|ionic|xamarin)"
find . -name "*.xcodeproj" -o -name "*.xcworkspace" -o -name "android" -o -name "pubspec.yaml" -o -name "package.json"
```
### 1.2 Mobile Technology Stack

iOS: Xcode project files, Swift/Objective-C, CocoaPods, SPM
Android: Gradle files, Java/Kotlin, Android manifest
Cross-platform: React Native, Flutter, Ionic, Cordova, Xamarin
Hybrid: Capacitor, PhoneGap, WebView-based apps

### 1.3 Project Structure Analysis

Platform-specific directories (ios/, android/, lib/, src/)
Shared code vs platform-specific code
Asset organization (images, fonts, configs)
Configuration files and build scripts

## Phase 2: Mobile Architecture & Patterns
### 2.1 App Architecture Pattern

iOS: MVC, MVP, MVVM, VIPER, Coordinator pattern
Android: MVVM, MVP, Clean Architecture, MVI
Cross-platform: Redux, BLoC, Provider, Riverpod, MobX
State management approach and data flow

### 2.2 Navigation & Routing
```bash # Find navigation/routing files
find . -name "*navigation*" -o -name "*router*" -o -name "*route*" | grep -v node_modules
```
Navigation patterns and libraries used
Screen/page organization and flow
Deep linking and URL routing setup
Tab navigation, stack navigation, drawer navigation

### 2.3 UI/UX Architecture

Design system and component library usage
Theme and styling approach
Responsive design and screen adaptation
Accessibility implementation

## Phase 3: Mobile-Specific Features Analysis
### 3.1 Device Integration
```bash # Look for native feature usage
grep -r -i "camera\|location\|bluetooth\|biometric\|push\|notification" . --include="*.js" --include="*.ts" --include="*.dart" --include="*.swift" --include="*.kt"
```
### 3.2 Native Features Inventory

Camera & Media: Photo capture, video recording, gallery access
Location Services: GPS, geofencing, maps integration
Sensors: Accelerometer, gyroscope, proximity, ambient light
Biometrics: Face ID, Touch ID, fingerprint authentication
Communications: Bluetooth, NFC, WiFi, cellular
System Integration: Contacts, calendar, photos, files

### 3.3 Platform Services

Push Notifications: FCM, APNs, notification handling
Analytics: Firebase, Mixpanel, custom tracking
Crash Reporting: Crashlytics, Sentry, Bugsnag
App Store Integration: In-app purchases, subscriptions, ratings

## Phase 4: Data & Backend Integration
### 4.1 Data Management
```bash# Find database and storage files
find . -name "*database*" -o -name "*storage*" -o -name "*sqlite*" -o -name "*realm*" -o -name "*core*data*"
```
Local storage solutions (SQLite, Realm, Core Data, Hive)
Caching strategies and offline support
Data synchronization patterns
Secure storage for sensitive data

### 4.2 Network & API Integration

REST API consumption patterns
GraphQL implementation (if used)
Authentication and token management
Network error handling and retry logic
API response caching and optimization

### 4.3 Security Implementation

API key and secret management
SSL pinning and certificate validation
Biometric and device-based authentication
Data encryption and secure storage
Reverse engineering protection

##  Phase 5: Mobile Performance & Optimization
5.1 Performance Patterns
```bash # Look for performance-related code
grep -r -i "lazy\|async\|await\|cache\|optimize\|performance" . --include="*.js" --include="*.ts" --include="*.dart" --include="*.swift" --include="*.kt"
````

 Lazy loading and code splitting
Image optimization and caching
Memory management patterns
Battery usage optimization
Network request optimization

##  Phase 6: Mobile Build & Deployment
6.1 Build Configurations

Build configurations (debug, release, staging)
Code signing and provisioning profiles
App store deployment setup
Continuous integration for mobile
Testing on devices and simulators

Phase 6: Mobile Testing Strategy
6.1 Testing Approach
bash# Find test files and configs
find . -name "*test*" -o -name "*spec*" -o -name "*.test.*" | grep -v node_modules
ls -la | grep -E "(test|spec|__tests__|cypress|detox|appium)"

Unit testing frameworks and coverage
Integration testing approach
UI/E2E testing (Detox, Appium, Espresso, XCTest)
Device testing matrix and strategy

6.2 Mobile-Specific Testing

Different screen sizes and orientations
Platform version compatibility
Network connectivity scenarios
Background/foreground app states
Permission handling and edge cases

Mobile Platform Specific Analysis:
iOS Specific (if detected):
bash# iOS project analysis
find . -name "*.xcodeproj" -exec ls -la {} \;
find . -name "Podfile" -o -name "Package.swift"
grep -r "@objc\|@IBAction\|@IBOutlet" . --include="*.swift"

Xcode project structure and targets
Swift vs Objective-C usage patterns
iOS SDK and framework usage
App Store Connect integration
iOS-specific UI patterns (UIKit, SwiftUI)

Android Specific (if detected):
bash# Android project analysis  
find . -name "build.gradle" -o -name "AndroidManifest.xml"
find . -name "*.kt" -o -name "*.java" | head -20
grep -r "import android\." . --include="*.kt" --include="*.java"

Gradle build system and modules
Kotlin vs Java usage patterns
Android SDK and API level usage
Google Play Console integration
Android-specific UI patterns (Activities, Fragments, Compose)

React Native Specific (if detected):
bash# React Native analysis
cat package.json | grep -i react
find . -name "index.js" -o -name "App.js" -o -name "metro.config.js"
ls -la ios/ android/ 2>/dev/null

React Native version and dependencies
Native module usage and bridges
Platform-specific code organization
Metro bundler configuration
Native iOS/Android integration

Flutter Specific (if detected):
bash# Flutter analysis
cat pubspec.yaml
find . -name "*.dart" | head -20
ls -la lib/ test/ ios/ android/ 2>/dev/null

Flutter SDK version and dependencies
Widget tree architecture
State management approach (BLoC, Provider, Riverpod)
Platform channel usage for native features
Build flavors and configurations

Comprehensive Mobile Output Format:
Mobile App Overview

App Type: [Native iOS, Native Android, Cross-platform, Hybrid]
Target Platforms: [iOS versions, Android API levels]
Architecture: [MVVM, Clean Architecture, Redux, etc.]
Primary Language: [Swift, Kotlin, Dart, JavaScript, etc.]
UI Framework: [UIKit, SwiftUI, Jetpack Compose, Flutter, React Native]

Mobile Feature Matrix
Feature CategoryImplementationPlatform SupportNotesAuthenticationOAuth 2.0, BiometricsiOS, AndroidFace ID, Touch ID supportPush NotificationsFCMCross-platformCustom notification handlingLocation ServicesNative GPSiOS, AndroidBackground location trackingCamera/MediaNative APIsCross-platformPhoto/video captureOffline SupportSQLite + SyncCross-platformConflict resolution strategy
Mobile Architecture Diagram
Mobile App Architecture:
├── Presentation Layer
│   ├── Screens/Views [UI components and navigation]
│   ├── State Management [Redux/BLoC/Provider patterns]
│   └── Theme/Styling [Design system implementation]
├── Business Logic Layer  
│   ├── Use Cases/Interactors [Business rules]
│   ├── Services [API communication, device features]
│   └── Models [Data structures and validation]
├── Data Layer
│   ├── Repositories [Data source abstraction]
│   ├── Local Storage [SQLite, Realm, Core Data]
│   └── Remote APIs [REST/GraphQL clients]
└── Platform Layer
    ├── Native Modules [Platform-specific code]
    ├── Device APIs [Camera, location, sensors]
    └── System Integration [Push, deep links, sharing]
Mobile Development Guide

Adding new screens: Navigation setup and state management
Integrating native features: Platform-specific implementation
Handling permissions: Runtime permission patterns
Testing approach: Device testing and automation
Build and deployment: App store submission process
Performance considerations: Mobile-specific optimizations

Mobile-Specific Recommendations

Performance: Bundle size, startup time, memory usage
User Experience: Offline functionality, loading states, error handling
Platform Guidelines: iOS HIG and Android Material Design compliance
Security: Secure storage, API security, code obfuscation
Accessibility: Screen reader support, dynamic type, high contrast
Store Optimization: App store listing, screenshots, keywords

Mobile Quality Checklist

 Runs on target iOS/Android versions
 Handles network connectivity changes
 Proper permission request flows
 Responsive to different screen sizes
 Efficient memory and battery usage
 Offline functionality where needed
 Push notifications working properly
 App store guidelines compliance
 Accessibility features implemented
 Security best practices followed