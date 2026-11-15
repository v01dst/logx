# logx

Analyze log files from your terminal. Tail, filter by level, search, count. Zero dependencies, pure Python stdlib.

## Install

```bash
pip install logx
```

Or run directly:

```bash
python logx.py --help
```

## Usage

```bash
# Last N lines
logx tail app.log -n 20

# Only errors and worse
logx filter app.log --level error

# Search with regex
logx search app.log "timeout|refused"

# Count per level
logx count app.log

# Level distribution
logx stats app.log
```

## Levels

`debug`, `info`, `warn`, `error`, `fatal`

## License

MIT