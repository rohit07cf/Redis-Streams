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
```

### Key Redis Stream Commands

#### XADD
Adds a new entry to a stream.
- Automatically generates a unique entry ID (timestamp-based)
- Creates the stream if it does not exist

#### XREAD
Reads entries from one or more streams.
- Used by simple consumers
- Does not support consumer groups or acknowledgments

#### XREADGROUP
Reads entries as part of a consumer group.
- Enables multiple consumers to process the same stream
- Supports message tracking and pending entries
- Requires explicit acknowledgment

#### XACK
Acknowledges that a message has been successfully processed.
- Removes the entry from the consumer group’s pending list

#### XLEN
Returns the total number of entries in a stream.

#### XRANGE
Retrieves a range of entries from a stream.
- Can be queried by start and end entry IDs

#### XTRIM
Limits the size of a stream.
- Used to cap memory usage
- Supports trimming by max length or by entry ID

## What is `BLOCK` in Redis Streams?

`BLOCK` is a parameter used with `XREAD` and `XREADGROUP` that tells Redis **how long to wait** for new stream entries when the stream is empty or the consumer has already caught up.

### How It Works
- The value is specified in **milliseconds**
- Redis holds the connection open until:
  - New entries arrive, or
  - The timeout expires

### Common Values
- `BLOCK 0` → Wait indefinitely (infinite block)
- `BLOCK 1000` → Wait up to 1 second
- No `BLOCK` → Return immediately (non-blocking)

### Behavior Comparison

**Non-blocking (no `BLOCK`):**
- Checks the stream
- If no new entries exist, returns immediately

**Blocking (`BLOCK` enabled):**
- Waits for new entries to arrive
- Returns as soon as data is available or timeout is reached

### Intuition (Mailbox Analogy)
- **Non-blocking:** Check the mailbox → empty → walk away
- **Blocking:** Stand by the mailbox and wait up to *X* seconds for mail to arrive

`BLOCK` is commonly used to build efficient, event-driven consumers without busy polling.
