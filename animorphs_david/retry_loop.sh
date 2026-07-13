#!/bin/bash
# Re-run pool_run (skips existing mp4s) until all 38 dv1 shots exist.
# 4 workers to play nice with the other batch sharing the 8-job limit.
cd /Users/dawndrain/Code/videogen
want=38
for pass in 1 2 3 4 5 6 7 8 9 10 11 12; do
  have=$(ls animorphs_david/outputs/dv1/*.mp4 2>/dev/null | wc -l | tr -d ' ')
  echo "pass $pass: $have/$want done"
  if [ "$have" -ge "$want" ]; then echo "ALLCOMPLETE"; exit 0; fi
  caffeinate -is python3 pool_run.py animorphs_david/videos_dv1.sh animorphs_david/outputs/dv1 4
  sleep 90
done
have=$(ls animorphs_david/outputs/dv1/*.mp4 2>/dev/null | wc -l | tr -d ' ')
echo "GAVEUP with $have/$want"
