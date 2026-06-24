Update setup-matt-pocock-skills in .agents .claud and agent-workflow
    change the name to setup-workflow-skills
    update any references to it
    update the labels to include hitl-unprepped, ready-for-agent-review, includes-front-end, agent-front-end-reviewed, agent-reviewed, ready-to-merge

Create new skills
    pr-review
    hitl-prep
    review implement to see if its correct

Split prompt, create select-items.md
    select-items returns all ready-for-agent without open dependencies, unprepped-hitl without dependencies, ready-for-agent-review and agent-reviewed
    change main.py to 
        spin up agent to run select-items
            If the only items available are issues awaiting dependencies pause and retry using an exponential back off with configurable initial and max waiting periods (default initial 5 minutes, default max 2 hours), after max waiting is hit stop the whole program with appropriate message too the user
            put all ready to merge in FIFO merge queue
            put everything else returned in FIFO work queue
        for each item in the work queue start a new coroutine, all coroutines should set a configurable timeout (default 30 minutes) that throws error that stops the main program with an appropriate error to the user to avoid infinite loops
            if ready-for-agent spin up agent to run tdd skill in a separate worktree then set ready-for-agent-review and if includes front end set includes-front-end, then add it to the FIFO work queue, timeout after configurable interval 
            if ready-for-agent-review spin up multiple sandboxed agents in parralel
                a security review agent
                a code review agent
                if includes-front-end, a front-end review agent
                a performance review agent
                when they all return success, set agent-reviewed and add it to the FIFO work queue
            if agent-reviewed, spin up agent to run tdd skill to implement fixes then label ready-to-merge and add it to the FIFO merge queue
            if unprepped-hitl spin up agent to run hitl-prep skill and set ready-for-human
        process merge FIFO queue in a single coroutine, for each item in merge queue, merge using resolving-merge-conflicts skill and if it goes on for longer than some configurable time (default 10 minutes) raise error that includes a the branch unable to merge and propagates up the error to the main program, the main program should then terminate all other running coroutines and sandboxes, remove any left over worktrees and related branches except the branch that caused the error that should be presevred, and return an informative error with the problematic branch to the user. We can always restart given the git labels on open issues, but this prevents infinite looping for complex merge requests and backing up of subsequent branches that may then also fail to merge. 
 