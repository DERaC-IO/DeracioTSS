![DeracioTSS](/misc/deractss_logo.png)

# Change Log

## Version 1.1.x

### 1.1.1

#### Implemented Enhancement(s)

- None

#### Fixued Bug(s)

- Error is fixed when no handler is registered in `DeracioTSS.health()` ([Issue #6](https://github.com/DERaC-IO/DeracioTSS/issues/6))

#### Housekeeping Change(s)

- None

### 1.1.0

#### Implemented Enhancement(s)

1. Routing/handler CLI manager
2. Settings CLI manager
3. System health checker (primitive)
4. Server stop/start switch

#### Fixued Bug(s)

- None

#### Housekeeping Change(s)

1. Opening menu
2. Much faster quick-starter options
3. Rationalizing questionaries

## Version 1.0.x

### 1.0.3

#### Implemented Enhancement(s)

- None

#### Fixued Bug(s)

1. An error to generate the shell script path while quick-starting has been fixed

#### Housekeeping Change(s)

- None

### 1.0.2

#### Implemented Enhancement(s)

1. Modified to manage route/handler in JSON file (`handler.json`) in `settings.d`
2. CLI options are added for quick-start

#### Fixued Bug(s)

- None

#### Housekeeping Change(s)

1. Revisions of asking questions including the one mentioned at [Issue #4](https://github.com/DERaC-IO/DeracioTSS/issues/4)
2. Re-coded as class instead of single function
3. Text decorations for CLI outputs

### 1.0.1

#### Implemented Enhancement(s)

1. Generating settings.py from JSON files in `settings.d` ([Issue #3](https://github.com/DERaC-IO/DeracioTSS/issues/3))

#### Fixued Bug(s)

- None

#### Housekeeping Change(s)

1. `version` parameter is added in `main` to display its version
