# update documentation command

Update documentation based on changes at module related (create or update readme at root module related).
or update documentation based on last commit (understanding the commit message for last 2 weeks) or based on changes, add or update file.
Update memory CLAUDE to reflect the latest changes or if in readme is updated dont update memory CLAUDE twice but reference it to read the updated documentation.
check if there are any README files in other modules that might need updates to maintain consistency.
if any README files are have information that same with the CLAUDE memory, update memory CLAUDE to give the link the README file for reference.
so that CLAUDE memory is always up to date with the latest documentation and consistent across all modules but memory is not duplicated.
keep memory token to below 39k characters.
keep README files max 39k characters.
the important part in readme is navigation related the module should exist (if not add navigation section)
and the endpoint being used in the module should be documented (if not add endpoint section)
and should be consistent across all modules
and update DESIGN_SYSTEM_RULES.md (max 39k characters) if needed.
give highlight and direct to read readme files for memory.
update DEPRECATION_ANALYSIS.md (max 39k characters) if needed (check superseded specs and update if necessary).
update .docs/c4/ (max 39k characters every files) if needed, see the files inside that folder and update if necessary.
do not create new files, only create or update files that mentioned in the command.