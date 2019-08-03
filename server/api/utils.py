def pop__sa_instance_state(query):
    output = []

    for each in query:
        dict = each.__dict__
        dict.pop('_sa_instance_state')
        output.append(dict)

    return output
