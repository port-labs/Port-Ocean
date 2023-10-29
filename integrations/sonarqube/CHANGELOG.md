# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

# Port_Ocean 0.1.5 (2023-10-22)

### Features

- Added a sanity check for sonarqube to check the sonarqube instance is accessible before starting the integration (PORT4908)

### Improvements

- Updated integration default port app config to have the `createMissingRelatedEntities` & `deleteDependentEntities` turned on by default (PORT-4908)
- Change organizationId configuration to be optional for on prem installation (PORT-4908)
- Added more verbose logging for the http request errors returning from the sonarqube (PORT-4908)
- Updated integration default port app config to have the  &  turned on by default (PORT4908)

### Bug Fixes

- Changed the sonarqube api authentication to use basic auth for on prem installations (PORT-4908)


# Sonarqube 0.1.4 (2023-10-15)

### Improvements

- Changed print in the http error handling to log info


# Sonarqube 0.1.3 (2023-10-04)

### Improvements

- Skip analysis resync for onpremise Sonarqube (#3)


# Sonarqube 0.1.2 (2023-09-27)

### Improvements

- Bumped ocean to version 0.3.1 (#1)


# Sonarqube 0.1.1 (2023-09-13)

### Improvements

- Bumped ocean to 0.3.0 (#1)

# Sonarqube 0.1.0 (2023-08-09)

### Features

- Implemented Sonarqube integration using Ocean
