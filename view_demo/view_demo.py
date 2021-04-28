### Sample script to create a view and assign a read only user to it
### Assumes
### * You've loaded the Imply View Manager extension
### * You're using Druid Basic Security
### * You've added VIEW permissions for the amdin user
### * You've got a wikipedia datasource
### See https://docs.imply.io/latest/druid/operations/row-and-column-security/

import requests, sys

if __name__ == "__main__":

    # Base URL for Druid.
    druid_base = "http://localhost:8081/"

    # Headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

    # API Login
    user = "admin"
    password = "password1"

    # View definition. Script uses the same name for the role
    view_name = "fr"
    view_definition = """
        {"viewSql": "SELECT __time, channel, page FROM wikipedia WHERE channel = '#fr.wikipedia'"}
        """
    # Permission to query the view
    view_permission = """
    [
    {
    "resource": {
        "name": "%s",
        "type": "VIEW"
    },
        "action": "READ"
    }
    ]"""%(view_name)

    # View read only user
    ro_user = "%s_user"%(view_name)
    ro_password = """
    {
        "password": "%s_password"
    }
    """%(view_name)

    try:
        # Create the view
        # POST http://localhost:8081/druid-ext/view-manager/v1/views/{view_name}
        # Include the view definition in the payload
        print("Creating view: %s\n"%(view_name))
        view_URL = druid_base+"druid-ext/view-manager/v1/views/%s"%(view_name)
        create_view = requests.post(view_URL, headers=headers, auth=(user, password), data=view_definition)
        print("Created view returned status code: %s\n"%(create_view.status_code))
        
        # If we get a 201 success code, it worked
        if (create_view.status_code == 201):
            print("Created view %s.\n"%(view_name))
        # Otherwise print the response body and exit
        else: 
            print(create_view.content)
            sys.exit("Couldn't create view.")

        # Create a role related to the view
        # Using the Coordinator Secuirty API
        # POST http://localhost:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/{role_name}
        
        print("Creating role: %s\n"%(view_name))
        role_URL = druid_base+"druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/%s"%(view_name)
        create_role = requests.post(role_URL, headers=headers, auth=(user, password))
        print("Create role returned status code: %s\n"%(create_role.status_code))
        
        # If we get a 200 success code, it worked
        if (create_role.status_code == 200):
            print("Created role %s.\n"%(view_name))
        # Otherwise print the response body and exit
        else:
            print(create_role.content)
            sys.exit("Couldn't create role.")
        
        # Add the permissions to the role
        # Using the Coordinator Secuirty API
        # POST http://localhost:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/{role_name}/permissions
        # Include the permissions in the payload
        print("Adding read only permissions to view %s for role: %s\n"%(view_name, view_name))
        role_permissions_URL = druid_base+"druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/roles/%s/permissions"%(view_name)
        add_permissions = requests.post(role_permissions_URL, headers=headers, auth=(user, password), data=view_permission)
        print("Adding view permissions returned status code: %s\n"%(add_permissions.status_code))

        # If we get a 200 success code, it worked
        if (create_role.status_code == 200):
            print("Added read only permissions to %s.\n"%(view_name))
        # Otherwise print the response body and exit
        else:
            print(create_role.content)
            sys.exit("Couldn't add permissions to role.")

        # Create the view read only user
        # Using the Coordinator Secuirty API
        # POST http://localhost:8081/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/{user name}
        print("Creating the read only user account: %s \n"%(ro_user))
        user_URL = druid_base+"druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/%s"%(ro_user)
        print(user_URL)
        add_user = requests.post(user_URL, headers=headers, auth=(user, password))
        print("Adding user returned status code: %s\n"%(add_user.status_code))

        # If we get a 200 success code, it worked
        if (add_user.status_code == 200):
            print("Added user %s.\n"%(ro_user))
        # Otherwise print the response body and exit
        else:
            print(add_user.content)
            sys.exit("Couldn't add user.")

        # Set the password for the view read only user
        # Using the Coordinator Secuirty API
        # POST http://localhost:8081/druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/{user name}/credentials
        print("Adding credentials for the read only user account: %s \n"%(ro_user))
        pass_URL = druid_base+"druid-ext/basic-security/authentication/db/MyBasicMetadataAuthenticator/users/%s/credentials"%(ro_user)
        add_pass = requests.post(pass_URL, headers=headers, auth=(user, password), data=ro_password)
        print("Adding user credentials returned status code: %s\n"%(add_pass.status_code))

        # 200 success code means it worked
        if (add_pass.status_code == 200):
            print("Added credentials for user %s.\n"%(ro_user))
        # Otherwise print the response body and exit
        else:
            print(add_pass.content)
            sys.exit("Couldn't add user credentials.")

        # Authoorize the view read only user
        # Using the Coordinator Security API
        # POST http://localhost:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/{user name}
        print("Authorizing the read only user account: %s \n"%(ro_user))
        auth_URL = druid_base+"druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/%s"%(ro_user)
        add_auth = requests.post(auth_URL, headers=headers, auth=(user, password))
        print("Authorizing status code: %s\n"%(add_auth.status_code))

        # 200 success code means it worked
        if (add_auth.status_code == 200):
            print("Authorize user %s.\n"%(ro_user))
        # Otherwise print the response body and exit
        else:
            print(add_auth.content)
            sys.exit("Couldn't authorize user.")


        # Add the view read only user to the role
        # Using the Coordinator Secuirty API
        # POST http://localhost:8081/druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/{user name}/roles/{role name}
        print("Adding the read only user account %s to the view role %s\n"%(ro_user, view_name))
        member_URL = druid_base+"druid-ext/basic-security/authorization/db/MyBasicMetadataAuthorizer/users/%s/roles/%s"%(ro_user, view_name)
        add_member = requests.post(member_URL, headers=headers, auth=(user, password))
        print("Adding user to role status code: %s\n"%(add_pass.status_code))

        # 200 success code means it worked
        if (add_member.status_code == 200):
            print("Added user %s to role %s.\n"%(ro_user, view_name))
        # Otherwise print the response body and exit
        else:
            print(add_member.content)
            sys.exit("Couldn't add user to role.")

        print("Login to the druid console as use: %s with password %s.\n"%(ro_user, ro_password))
        print("On the Query tab, you can see and query the %s view.\n"%(view_name))

    # In case of disaster         
    except Exception as e:
        sys.exit("Ouch! %s."%(e))