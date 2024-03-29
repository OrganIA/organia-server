#!/bin/sh

[ -d .venv ] && . .venv/bin/activate

cmd="alembic merge" && \
echo "$(alembic heads)" > merging_cache && \
while read l; do
    cache=$(echo "$l" | head -c 12)
    export cmd="$cmd $cache "
done < merging_cache && \
rm merging_cache && $cmd
