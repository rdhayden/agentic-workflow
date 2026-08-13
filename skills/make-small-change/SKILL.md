---
name: make-small-change
description: "Plan and implement a small change in one shot"
disable-model-invocation: true
---

Run the /auto-grilling skill with the requirement provided by the user
When auto-grilling completes run the /to-tickets skill and specify that it should be **fully automated**
When to-tickets completes run the /implement skill in a sub-agent for each of the tickets created by /to-tickets
When all tickets have been implemented run the /commit-and-review skill