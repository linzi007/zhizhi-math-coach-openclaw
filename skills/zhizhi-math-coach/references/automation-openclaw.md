# OpenClaw Automation

## Boundary

Scheduled tasks should default to reminders and suggestions. They should not automatically change weak-point status, memory, records, or generate new worksheets unless the parent has explicitly requested that behavior.

## Recommended Schedule

- Daily 20:30 Asia/Shanghai: due review reminders, pending upload reminders, and stale short-term observations.
- Sunday 20:00 Asia/Shanghai: weekly progress review and next-week suggestions.
- End of semester: generate a summary and holiday review pool.
- Winter/summer break: weekly holiday review suggestions.

## Suggested Task Outputs

- due weak points;
- pending worksheets not yet graded;
- short explanation cards that may help parents;
- suggested next worksheet strategy;
- warnings about low-confidence or missing evidence.

## Channels

The learning logic should not depend on a channel. Start with local records and OpenClaw conversation output.

For push delivery, use a channel adapter. Feishu/Lark is the default v1 recommendation when available because it supports chat, files, and operational workflows. DingTalk can be added later through a channel/plugin adapter if the environment supports it.

## Safety

- Do not send private student files to public channels.
- Do not push full answer keys into a child-facing chat.
- Do not infer new mastery status from time alone.
- Do not schedule automatic worksheet generation by default.
