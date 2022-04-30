import socket

def getMTAServerPlayers(ip, port, timeout=15):
    """
    Get a list of players from an MTA server using the ASE's server protocol.
    :param ip: The ip address of the MTA server
    :param port: The main port of the MTA server
    :param timeout: The number of seconds until timeout
    :return: A list of players
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        ase_port = port + 123

        sock.sendto(b"s", (ip, ase_port))
        result = sock.recv(4096)

        result = result.decode("utf8").replace('EYE1\x04mta', '')

        i = 0

        ## Port
        port_n = ord(result[i])
        i += port_n

        ## Server name
        server_name_n = ord(result[i])
        i += server_name_n

        ## Game type
        game_type_n = ord(result[i])
        i += game_type_n

        ## Map name
        map_name_n = ord(result[i])
        i += map_name_n

        ## Version
        version_n = ord(result[i])
        i += version_n

        ## Passworded
        passworded_n = ord(result[i])
        i += passworded_n

        ## Player count
        player_count_n = ord(result[i])
        i += player_count_n

        ## Player max
        player_max_n = ord(result[i])
        i += player_max_n

        ## TODO: Announcement rules

        ## Start of player stats
        i += 1

        ## For each player:
        players = []

        while i < len(result):
            ## Flag
            i += 1

            # Nick
            player_name_n = ord(result[i])
            player_name_str = result[i+1:i+player_name_n]
            i += player_name_n

            # team (skip)
            i += 1

            # skin (skip)
            i += 1

            # score
            score_n = ord(result[i])
            i += score_n

            #ping
            ping_n = ord(result[i])
            ping_str = result[i+1:i+ping_n]
            i += ping_n

            #time (skip)
            i += 1

            players.append({
                "name": player_name_str,
                "ping": int(ping_str)
            })
        return players, None
    except Exception as e:
        return False, e

