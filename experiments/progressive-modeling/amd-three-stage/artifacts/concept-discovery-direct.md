## Groups
group_id | name
G001 | operations
G002 | human_resources
G003 | customers
G004 | products
G005 | marketing
G006 | finance
G007 | assets
G008 | administration
G009 | security

## Concepts
concept_id | term | group_id | ambiguous
C001 | move | G001 | false
C002 | route | G001 | false
C003 | time_slot | G001 | false
C004 | fulfillment_event | G001 | false
C005 | address | G001 | true
C006 | staff_registry | G002 | false
C007 | job_assignment | G002 | true
C008 | worked_hours | G002 | false
C009 | payroll_calculation | G002 | false
C010 | bonus | G002 | false
C011 | leave | G002 | false
C012 | customer | G003 | false
C013 | contact | G003 | false
C014 | billing_information | G003 | false
C015 | billing_history | G003 | true
C016 | product | G004 | false
C017 | service | G004 | true
C018 | configuration | G004 | false
C019 | pricing | G004 | false
C020 | campaign | G005 | false
C021 | discount_code | G005 | false
C022 | lead | G005 | false
C023 | conversion_metric | G005 | false
C024 | payment | G006 | false
C025 | invoice | G006 | false
C026 | expense | G006 | false
C027 | vat | G006 | false
C028 | vehicle | G007 | false
C029 | equipment | G007 | false
C030 | consumable | G007 | false
C031 | maintenance | G007 | false
C032 | contract | G008 | false
C033 | insurance | G008 | false
C034 | document | G008 | true
C035 | audit_log | G008 | false
C036 | role | G009 | true

## Relations
from_concept_id | verb | to_concept_id
C001 | uses | C002
C001 | scheduled_in | C003
C001 | generates | C004
C001 | located_at | C005
C006 | performs | C007
C006 | logs | C008
C008 | feeds | C009
C009 | includes | C010
C006 | takes | C011
C012 | has | C013
C012 | provides | C014
C012 | has | C015
C016 | includes | C017
C016 | has | C018
C018 | determines | C019
C020 | generates | C022
C020 | uses | C021
C022 | tracked_by | C023
C024 | settles | C025
C025 | includes | C027
C026 | recorded_in | C006
C028 | undergoes | C031
C029 | undergoes | C031
C030 | consumed_by | C001
C032 | covers | C001
C033 | protects | C028
C034 | attached_to | C032
C035 | records | C001
C036 | assigned_to | C006

## Unresolved Terms
term | candidate_concept_ids
role | C036
address | C005
service | C017
document | C034
history | C015
assignment | C007
