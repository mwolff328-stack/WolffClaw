# Daily Spend Cron Notes

## Discord bot token path
The cron template uses `d['channels']['discord']['token']` but the actual path is:
```
d['channels']['discord']['accounts']['default']['token']
```
Fix the cron template if it gets regenerated.
