# Corpus Engine
Vector Embedding Powered Corpus Search Engine

# Use

```
engine <command>
```
## Example
```
engine init
rm -rf <example file>
engine update
engine query
engine remove
```

## Commands
- init
   - Initializes corpus engine into CWD and parses any current file inside of it

- query
    - Allows for user queries to search all supported files inside of CWD (and internal directories)

- update
    - Updates all changed, new, or removed files in database

- remove
    - Removes corpus engine from CWD

- reset
    - Performs remove and init actions sequentially


# Build

Build in project root using:
```
uv tool install .
```

Dev build using:
```
uv tool install -e .
```