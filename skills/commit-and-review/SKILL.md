---
name: commit-and-review
description: commit changes and generate review tickets for the user to review the architecture, tests and functionality
---

Commit all uncommited work in the current branch with an appropriate commit message

Once the commit is complete create a human in the loop (HITL) architecture and test review ticket for an engineer to review what has been implemented. Use the /c4-diagram skill to add c4 diagrams to the ticket and the /c4-to-text skill to describe the architecture as text in case the user cannot render the diagram well. The c4 diagrams and text should be scoped to the changes in this commit, only including components in the level 3 component tables and diagram that have changed or been implemented in this commit and neighboring components that are relevant to this commit

Extend the level 3 component relationship table to include a column called tests which lists all the tests related to each relationship. Below the component relationship table also add a brief description of each test so that the engineer can review all relationships created or updated and whether they are tested appropriately.

Create a human in the loop (HITL) functionality review ticket which has a checklist describing all the new capabilities that were implemented that the user can and should test manually along with a description of how they can test it

Provide the user with links to the architecture and test review ticket, and the functionality review ticket.