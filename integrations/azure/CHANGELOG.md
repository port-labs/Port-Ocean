0.1.42 (2024-04-11)

### Improvements

- Bumped ocean version to ^0.5.11 (#1)


0.1.41 (2024-04-10)

### Bug Fixes

- Fixed blueprints identifiers names and adjusted relations between blueprints


0.1.40 (2024-04-10)

### Improvements

- Bumped ocean version to ^0.5.10 (#1)


0.1.39 (2024-04-06)

### Features

- Added support for multiple azure subscriptions (#1)
- Added generic cloudResource kind (#2)

### Improvements

- Changed default blueprints and mapping to use the new generic cloudResource kind (#3)


0.1.38 (2024-04-01)

### Improvements

- Bumped ocean version to ^0.5.9 (#1)


0.1.37 (2024-03-28)

### Improvements

- Bumped ocean version to ^0.5.8 (#1)


0.1.36 (2024-03-27)

### Improvements

- Added default permissions to match the default resources created (#1)


0.1.35 (2024-03-20)

### Improvements

- Bumped ocean version to ^0.5.7 (#1)


0.1.34 (2024-03-17)

### Improvements

- Bumped ocean version to ^0.5.6 (#1)


0.1.33 (2024-03-06)

### Improvements

- Bumped ocean version to ^0.5.5 (#1)


0.1.32 (2024-03-03)

### Improvements

- Bumped ocean version to ^0.5.4 (#1)


0.1.31 (2024-03-03)

### Improvements

- Bumped ocean version to ^0.5.3 (#1)


0.1.30 (2024-02-21)

### Improvements

- Bumped ocean version to ^0.5.2 (#1)


0.1.29 (2024-02-20)

### Improvements

- Bumped ocean version to ^0.5.1 (#1)


0.1.28 (2024-02-18)

### Improvements

- Bumped ocean version to ^0.5.0 (#1)


0.1.27 (2024-01-23)

### Improvements

- Bumped ocean version to ^0.4.17 (#1)


0.1.26 (2024-01-11)

### Improvements

- Bumped ocean version to ^0.4.16 (#1)


0.1.25 (2024-01-07)

### Improvements

- Bumped ocean version to ^0.4.15 (#1)


0.1.24 (2024-01-07)

### Improvements

- Bumped ocean version to ^0.4.14 (#1)


0.1.23 (2024-01-01)

### Improvements

- Bumped ocean version to ^0.4.13 (#1)


v0.1.22 (2023-12-25)

### Improvements

- Fix stale relation identifiers in default blueprints (port-5799)


v0.1.21 (2023-12-24)

### Improvements

- Updated default blueprints and config mapping to include integration name as blueprint identifier prefix
- Bumped ocean version to ^0.4.12 (#1)


0.1.20 (2023-12-21)

### Improvements

- Bumped ocean version to ^0.4.11 (#1)


0.1.19 (2023-12-21)

### Improvements

- Bumped ocean version to ^0.4.10 (#1)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# 0.1.18 (2023-12-15)

### Improvements

- Introduced delete azure resources on delete event "best effort" capability (PORT-5643)


# 0.1.17 (2023-12-14)

### Improvements

- Bumped ocean version to ^0.4.8 (#1)


# 0.1.16 (2023-12-05)

### Improvements

- Bumped ocean version to ^0.4.7 (#1)


# 0.1.15 (2023-12-04)

### Improvements

- Bumped ocean version to ^0.4.6 (#1)


# 0.1.14 (2023-11-30)

### Improvements

- Bumped ocean version to ^0.4.5 (#1)


# 0.1.13 (2023-11-29)

### Improvements

- Bumped ocean version to ^0.4.4 (#1)


# 0.1.12 (2023-11-21)

### Improvements

- Bumped ocean version to ^0.4.3 (#1)


# 0.1.11 (2023-11-08)

### Improvements

- Bumped ocean version to ^0.4.2 (#1)


# 0.1.10 (2023-11-03)

### Improvements

- Bumped ocean version to ^0.4.1 (#1)


# 0.1.9 (2023-11-01)

### Improvements

- Bumped ocean version to ^0.4.0 (#1)


# 0.1.8 (2023-10-29)

### Improvements

- Bumped ocean version to 0.3.2 (#1)


# 0.1.7 (2023-09-27)

### Improvements

- Bumped ocean to version 0.3.1 (#1)


# 0.1.6 (2023-09-13)

### Improvements

- Bumped ocean version to 0.3.0 (#1)


# 0.1.5 (2023-08-29)

### Improvements

- Bumped ocean from 0.2.1 to 0.2.3 (PORT-4527)


# 0.1.4 (2023-08-22)

### Bug Fixes

- Added event_grid_system_topic_name and event_grid_event_filter_list to the spec.yaml extra vars (#1)


# 0.1.3 (2023-08-22)

### Bug Fixes

- Fixed subscriptionID description in the spec.yaml


# 0.1.2 (2023-08-21)

### Bug Fixes

- Aligned the deployment method attribute in spec.yaml to our new terraform module architecture


# 0.1.1 (2023-08-20)

### Bug Fixes

- Removed capability to remove port entity on received event of resource deletion
- Changed deployment method to point to full terraform module path

# 0.1.0 (2023-08-13)

### Features

- Added Azure ocean integration [PORT-4351] (#0)
