# Redis-Streams

## Core Concepts

### Stream
An ordered, append-only collection of entries.  
Each entry has a **unique ID**, which is timestamp-based by default.

### Consumer Groups
A mechanism that allows **multiple consumers** to read from the same stream while:
- Distributing messages across consumers (load balancing)
- Tracking delivery state
- Requiring explicit message acknowledgment

This enables scalable and reliable message processing.

### Entry ID
Each stream entry has an auto-generated ID in the format:

<millisecondTimestamp>-<sequenceNumber>

**Example:**
1706745600000-0


- `millisecondTimestamp`: Time when the entry was added
- `sequenceNumber`: Ensures uniqueness when multiple entries are added in the same millisecond

## Run Redis via Docker

Use Docker to quickly start a local Redis instance for development.

### Start Redis

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7

## Key Redis Stream Commands

### XADD
Adds a new entry to a stream.
- Automatically generates a unique entry ID (timestamp-based)
- Creates the stream if it does not exist

### XREAD
Reads entries from one or more streams.
- Used by simple consumers
- Does not support consumer groups or acknowledgments

### XREADGROUP
Reads entries as part of a consumer group.
- Enables multiple consumers to process the same stream
- Supports message tracking and pending entries
- Requires explicit acknowledgment

### XACK
Acknowledges that a message has been successfully processed.
- Removes the entry from the consumer group’s pending list

### XLEN
Returns the total number of entries in a stream.

### XRANGE
Retrieves a range of entries from a stream.
- Can be queried by start and end entry IDs

### XTRIM
Limits the size of a stream.
- Used to cap memory usage
- Supports trimming by max length or by entry ID