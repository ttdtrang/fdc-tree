import re, json

nodes = []
parents = []
with open('fdc.txt', 'r') as f:
    previousNode = {}
    for line in f:
        if ( line[0] == '#'): continue
        if (line.strip() and line.strip()[0] == '#'): continue
        m = re.search("(\s*)(\d+\S+)\s(.+)$",line)
        if (m):
            myLevel = len(m.group(1))
            thisNode =  {'id': m.group(2), 'text': "%s - %s" % (m.group(2),m.group(3)), 'level': myLevel }
            if (myLevel == 0):
                thisNode['parent'] = '#'
            else:
                myParent = thisNode['id']
                if (len(myParent) <= 3):
                    myParent = myParent[: myLevel] + '0' + myParent[myLevel+1:]
                elif (myParent.find('.') > 0):
                    myParent = myParent[: myParent.find('.') ]
                elif (myParent.find('-') > 0):
                    myParent = myParent[: myParent.find('-')]
                    myParent = myParent[: myLevel] + '0' + myParent[myLevel+1:]
                else:
                    print("Unhandled: %s" % line)
                thisNode['parent'] = myParent
            parents.append(thisNode['parent'])
            nodes.append(thisNode)

with open('fdc-jstree.json', 'w') as fw:
    fw.write( json.dumps(nodes))

parents = set(parents)
node_ids = [x['id'] for x in nodes]
# sanity check: make sure every "parent" is a valid node, root node # is certainly valid
for parent in parents:
    if (parent != '#' and (not (parent in node_ids))):
        print("Invalid parent: %s" % parent)
