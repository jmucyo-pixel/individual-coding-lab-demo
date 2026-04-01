#!/bin/bash

ORIGINAL="grades.csv"

# 1. Check/Create Archive Directory
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Created archive directory."
fi

# 2. Generate Timestamp
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

# 3. Check the source file exists before doing anything
if [ ! -f "$ORIGINAL" ]; then
    echo "Error: $ORIGINAL does not exist. Nothing to archive."
    exit 1
fi

# 4. Archival Process — rename and move to archive
mv "$ORIGINAL" "archive/$ARCHIVED_NAME"

if [ $? -ne 0 ]; then
    echo "Error: Failed to move $ORIGINAL to archive."
    exit 1
fi

echo "Archived: $ORIGINAL → archive/$ARCHIVED_NAME"

# 5. Workspace Reset — create a fresh empty grades.csv
touch "$ORIGINAL"
echo "Reset: fresh $ORIGINAL created."

# 6. Logging — append entry to organizer.log
LOG_ENTRY="[$TIMESTAMP] Original: $ORIGINAL | Archived as: archive/$ARCHIVED_NAME"
echo "$LOG_ENTRY" >> organizer.log
echo "Logged to organizer.log."

