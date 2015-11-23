import os

if __name__ == "__main__":
    config_path = os.path.dirname(os.path.realpath(__file__))
    print config_path
    if os.path.exists(config_path + "/config.py"):
        print "config.py already exists."
    else:
        print "Need to set up config file.\n"
        user = raw_input("DB User: ")
        pw = raw_input("DB Password: ")
        with open('config.py', 'w') as f:
            f.write("DB_USER = '%s'\n" % user +
                    "DB_PW = '%s'\n" % pw +
                    "DB_SCHEMA = 'stuffnetwork'\n" +
                    "DB_HOST = 'localhost'\n")
        print "Created config.py. Defaulted host and schema name to localhost and stuffnetwork."

