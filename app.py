from dynatrace import Dynatrace

# Create a Dynatrace client
dt = Dynatrace("https://abc12345.live.dynatrace.com", "dt0c01.*****")


def find_relationships(frm, frm_name, to, frm_relationship):
    discovered_to_entities = []
    to_ids = []

    for entity in dt.entities.list(f"type({frm}),entityName.equals({frm_name})", fields="fromRelationships"):
        # If this entity does not have a matching frm_relationship, skip it. Dont care about it.
        if frm_relationship not in entity.from_relationships:
            continue
        for to_entity in entity.from_relationships[frm_relationship]:
            # Add this to_entity to the ID list
            to_ids.append(to_entity.id)
    
    for to_id in to_ids:
        for to_entity in dt.entities.list(f"type({to})"):
            if to_entity.entity_id == to_id:
                #print(f"Found match for {to_id}. Name is: {to_entity.display_name}")
                discovered_to_entities.append(to_entity)

    return discovered_to_entities 
    

#########################
# Start main logic...
#########################
frm_level_1 = "APPLICATION"
frm_name_level_1 = "MyApp - Prod"
frm_relationship_level_1 = "calls"
to_level_1 = "SERVICE"
frm_level_2 = "SERVICE"
frm_relationship_level_2 = "runsOnHost"
to_level_2 = "HOST"

discovered_entities = find_relationships(frm=frm_level_1, frm_name=frm_name_level_1, frm_relationship=frm_relationship_level_1, to=to_level_1)

print('Printing the first level...')

for found_entity in discovered_entities:
    print(f"{found_entity.display_name} has ID: {found_entity.entity_id}")
    
    # Now for each of these entities, find the next level down
    discovered_entities_2 = find_relationships(frm='SERVICE', frm_name=found_entity.display_name,frm_relationship='runsOnHost', to='HOST')

    print('----------')
    print('Printing the next level down...')
    for found_entity_2 in discovered_entities_2:
        print(f"{found_entity_2.display_name} has ID: {found_entity_2.entity_id}")
        print(f"This means that {frm_name_level_1} runs on {found_entity_2.display_name} with ID: {found_entity_2.entity_id}")
