# CHANGELOG
# ref: http://keepachangelog.com/en/0.3.0/
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

Example
## [0.0.x] 2017-04-26
### Added
  - Add LICENSE file
### Changed
  - Changed LICENSE from MIT to Apache
### Fixed
  - Fixed the missing copyright details in LICENSE file

## [1.2.0] 2017-10-26
### Summary
  - This release addresses the need to have specific version of dependencies
### Added
  - add a 'v' option to the docstring (Matthew McConnell)
  - add specific versions of dependencies (Matthew McConnell)

## [1.1.0] 2017-08-14
### Summary
  - This release adds hawkeye interoperability, allowing Linemans logs to be consumed by Hawkeye and 
    emailed out.
### Added
  - have hawkeye interop use a setting called template version, and some code clean up (Matthew McConnell)
  - add unit tests to test hawk_eye interop (Matthew McConnell)
  - Change the CHANGELOG to a md filetype for github to display it better (Matthew McConnell)
  - update setup with a new way to read in version, the proper license, and proper url (Matthew McConnell)
  - Add a source key to the output log for consumption by hawk-eye (Matthew McConnell)

### CHANGED
  - fix how main imports version (Matthew McConnell)
  - Recreate the TODO as an org file (Matthew McConnell)
  - update description so humans can understand it. (Christopher Barnes)

## [1.0.0] 2017-04-26

 * Summary:
  This is the initial release of lineman, a tool to ensure JSON data is properly
  formatted to go into REDCAP  
 * add project TODO with examples, references and formating (Christopher Barnes)
 * add CHANGELOG with format, references and examples (Christopher Barnes)
 * change LICENSE form MIT to Apache and update copyright to point to AUTHORS file (Christopher Barnes)
 * add authors matt and buck to formated file (Christopher Barnes)
 * add authors formated file (Christopher Barnes)
 * adjust logs to be more readable (Patrick White)
 * docopt unit testing refactor (Patrick White)

 * bugfix (Patrick White)
 * fixes more subject events than there are events to map to (Patrick White)
 * casting the response content as string (Patrick White)
 * fixed report generation bugs (Patrick White)
 * added initial report functionality (Patrick White)
 * faster export records call (Patrick White)
 * changes to make lineman a command line tool (Patrick White)
 * add __init__.py (Patrick White)
 * Files added (Patrick White)
 * Initial commit (PFWhite)
