def build_user_dict(userInfo):
    # UID, FNAME, LNAME, CDATE, CTIME, PSEUDONYM
    user = {}
    print(userInfo)
    user["uID"] = userInfo[0]
    user["fName"] = userInfo[1]
    user["lName"] = userInfo[2]
    user["utime"] = userInfo[3]
    user["pseudonym"] = userInfo[4]
    return user

def build_reacted_user_dict(userInfo):
    # UID, FNAME, LNAME, CDATE, CTIME, PSEUDONYM
    user = {}
    print(userInfo)
    user["uID"] = userInfo[0]
    user["fName"] = userInfo[1]
    user["lName"] = userInfo[2]
    user["utime"] = userInfo[3]
    user["pseudonym"] = userInfo[4]
    user["rtime"] = userInfo[5]
    return user

def build_credential_dict(userCredential):
    # UID, Username, Password, UEmail, UPhone
    cred = {}
    cred["uID"] = userCredential[0]
    cred["username"] = userCredential[1]
    cred["password"] = userCredential[2]
    cred["uEmail"] = userCredential[3]
    cred["uPhone"] = userCredential[4]
    return cred

def build_activity_dict(userActicity):
    # AID, lastAccessToDBDate, lastAccessToDBTime, isActive
    activity = {}
    activity["uID"] = userActicity[0]
    activity["lastimeaccesstimestamp"] = userActicity[1]
    activity["isActive"] = userActicity[2]


    return activity

def build_contact_dict(userContact):
    # ownerid, memberid
    contact = {}
    contact["uid"] = userContact[0]
    contact["memberID"] = userContact[1]
    return contact

def build_chat_dict(chat):
    # cid, cname, ctime, isgroupchat, isactive, adminid
    chatRecord = {}
    print(chat)
    chatRecord["cID"] = chat[0]
    chatRecord["cName"] = chat[1]
    chatRecord["cTime"] = chat[2]
    chatRecord["isGroupChat"] = chat[3]
    chatRecord["isActive"] = chat[4]
    chatRecord["uID"] = chat[5]
    return chatRecord

def build_participants_dict(chatParticipant):
    # uid, cid, ptime

    participant = {}
    print(chatParticipant)
    participant["uID"] = chatParticipant[0]
    participant["cID"] = chatParticipant[1]
    participant["pTime"] = chatParticipant[2]
    return participant

def build_message_dict(chatMessage):
    # mid, text, cdate, ctime, cid, uid, isdeleted, rid
    Message = {}
    print(chatMessage)
    Message["mID"] = chatMessage[0]
    Message["text"] = chatMessage[1]
    Message["mTime"] = chatMessage[2]
    Message["uID"] = chatMessage[3]
    Message["cID"] = chatMessage[4]
    Message["isDeleted"] = chatMessage[5]
    Message["rID"] = chatMessage[6]
    return Message

def build_extended_message_dict(chatMessage):
    # mid, text, cdate, ctime, cid, uid, isdeleted, rid
    Message = {}
    print(chatMessage)
    Message["mID"] = chatMessage[0]
    Message["text"] = chatMessage[1]
    Message["mTime"] = chatMessage[2]
    Message["pseudonym"] = chatMessage[3]
    Message["uID"] = chatMessage[4]
    Message["cID"] = chatMessage[5]
    Message["isDeleted"] = chatMessage[6]
    Message["rID"] = chatMessage[7]
    Message["likes"] = chatMessage[8]
    Message["dislikes"] = chatMessage[9]

    return Message

def build_reacted_dict(messageReaction):
    # uid, mid, rdate, rtime, vote
    reaction = {}
    reaction["uID"] = messageReaction[0]
    reaction["mID"] = messageReaction[1]
    reaction["rTime"] = messageReaction[2]
    reaction["vote"] = messageReaction[3]

    return reaction

def build_topic_dict(messageTopic):
    # tid, hashtag, mid, ttime
    topic = {}
    topic["tID"] = messageTopic[0]
    topic["hashtag"] = messageTopic[1]
    topic["mID"] = messageTopic[2]
    topic["ttime"] = messageTopic[3]
    return topic

def build_media_dict(messageMedia):
    # mid, mediaid, isVideo, location
    media = {}
    media["mID"] = messageMedia[0]
    media["isVideo"] = messageMedia[1]
    media["location"] = messageMedia[2]
    return media


def build_dash_topic_dict(topicsInDay):
    topic = {}
    topic["hashtag"] = topicsInDay[0]
    topic["total"] = topicsInDay[1]
    return topic


def build_dash_message_dict(topicsInDay):
    topic = {}
    topic["Message"] = topicsInDay[0]
    topic["total"] = topicsInDay[1]
    return topic


def build_dash_user_dict(usersInDay):
    users = {}
    users["username"] = usersInDay[0]
    users["totalmessages"] = usersInDay[1]
    return users