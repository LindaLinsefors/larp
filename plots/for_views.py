from django import forms

def checkboxes(choice_list):
    return forms.MultipleChoiceField(
                    required = False,
                    widget  = forms.CheckboxSelectMultiple , 
                    choices = [ (choice, choice.name) 
                                for choice
                                in choice_list   ] )

def save_relations( instance,
                    choice_list, old_relations, new_relation_names,  
                    RelationClass, instance_type, choice_type ):

    for choice in choice_list:
        if (        (choice not in old_relations) 
                and (choice.name in new_relation_names) ):
            RelationClass(**{choice_type:choice, instance_type:instance}).save()
        elif (      (choice in old_relations) 
                and (choice.name not in new_relation_names) ):
            RelationClass.objects.get(**{choice_type:choice, instance_type:instance}).delete()        
            


