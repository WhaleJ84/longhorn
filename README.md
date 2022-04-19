# Longhorn

A network automation application that performs a series of actions from an initiating request.
Designed around circuit outage remediation, Longhorn aims to create an end-to-end pipeline, from verifying outage to contacting the relevant parties.

## Technologies

Longhorn integrates with a number of technologies to tie the services together.
Currently included technologies are as follows:

- Email
  - Used to inform users of the actions performed
  - Contacts relevant parties that accept email communication
- Netbox
  - Searches for the affected circuit within Netbox
  - Determines who maintains the circuit
  - Retrieves their preferred contact method
  - Analyses journal entries for noted tickets or changes
- Faveo
  - Queries database for ticket found in Netbox
  - Verifies ticket is still in an open state
  - Opens ticket if one does not exist
  - Updates ticket with performed actions

## Testing Locally

The following steps are to remind myself of all requirements in the project thus far.
For others attempting to recreate this, own instances of Faveo and Netbox are required (they're both free).

1) Run local mail-server: `sudo mailhog --smtp-bind-addr 127.0.0.1:25`
2) Ensure Faveo and Netbox servers are running
3) Run Longhorn
4) Send in request
5) Verify output in [email](http://localhost:8025)
