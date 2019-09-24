"""
This Class contains DAO methods for the entities of Messages, Medias, Topics and Reacted
"""
from pg_config import pg_config
import psycopg2


class MessagesDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % \
                         (pg_config['dbname'], pg_config['user'], pg_config['passwd'],
                          pg_config['port'], pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    # ====================== Create Method ================================================== #
    def insertMessage(self, text, uid, cid, rid):
        # Create a message to a chat
        cursor = self.conn.cursor()
        query = "select count(*) from participants where cid = %s and uid = %s;"
        cursor.execute(query, (cid, uid))
        count = cursor.fetchone()
        self.conn.commit()
        if count[0] == 0:
            return None
        else:
            if rid:
                query2 = "select text from messages where mid = %s;"
                cursor.execute(query2, (rid,))
                rtext = cursor.fetchone()
                self.conn.commit()
                if rtext:
                    text = "RE:\" " + str(rtext[0]) + " \" " + text

            query3 = "insert into messages(text,mtime,uid,cid,isDeleted, rid) values(%s,'now',%s,%s,'f',%s) returning mid;"
            cursor.execute(query3, (str(text), uid, cid, rid))
            self.conn.commit()
            mid = cursor.fetchone()
            query5 = "update activities set lastdbaccesstimestamp = 'now', isactive = 't' where uid = %s;"
            cursor.execute(query5, (uid,))
            self.conn.commit()
            listOfStrings = str(text).split()
            for word in listOfStrings:
                if word.find('#') != -1:
                    self.insertTopic(mid, word.replace('#', ''))
            return mid

    def insertReacted(self, uid, mid, vote):
        # Create a message to a chat
        cursor = self.conn.cursor()
        query3 = "select * from participants where cid = (select cid from messages where mid =%s ) and uid =%s;"
        cursor.execute(query3,(mid,uid))
        userInCHat = cursor.fetchone()
        self.conn.commit()
        query = "select count(*) from reacted where uid = %s and mid = %s "
        cursor.execute(query, (uid, mid))
        count = cursor.fetchone()
        self.conn.commit()
        print(count)
        if count[0] != 0 or not userInCHat:
            return None
        else:
            query2 = "insert into reacted values(%s, %s, 'now', %s) returning rtime"
            cursor.execute(query2, (str(uid), str(mid), str(vote)))
            self.conn.commit()
            rtime = cursor.fetchone()
            query5 = "update activities set lastdbaccesstimestamp = 'now', isactive = 't' where uid = %s;"
            cursor.execute(query5, (uid,))
            self.conn.commit()
            return rtime

    def insertTopic(self, mid, hashtag):
        # Create a message to a chat
        cursor = self.conn.cursor()
        query1 = "insert into topics(hashtag, mid, ttime) values(%s, %s, 'now') returning tid"
        cursor.execute(query1, (str(hashtag), mid))
        self.conn.commit()
        tid = cursor.fetchone()
        return tid

    def insertMedia(self, mID, isVideo, location):
        # Add media to a message
        medID = 3
        return mID, medID

    # ====================== Get Message Records ============================================ #
    # =============== Single Record Queries ==================== #
    def getMessageInfo(self, mID):
        cursor = self.conn.cursor()
        query = "select * from messages where mid = %s;"
        cursor.execute(query, (mID, ))
        result = cursor.fetchone()
        return result

    def getRepliedMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select * from messages where mid = (select rid from messages where mid = %s);"
        cursor.execute(query, (mID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def searchAllChatMessages(self, cID, search):
        cursor = self.conn.cursor()
        query = "with like_messages as " \
                "(with like_reacted as (select * from reacted where vote = 1)" \
                "(select mid, text, mtime, messages.uid, cid, isdeleted, rid, count(vote) as likes" \
                " from messages left join like_reacted using(mid)" \
                " group by mid, text, mtime, messages.uid, cid, isdeleted, rid" \
                " order by mtime)), dislike_messages as " \
                " (with dislike_reacted as (select * from reacted where vote = -1)" \
                " (select mid, text, mtime, messages.uid, cid, isdeleted, rid, count(vote) as dislikes" \
                " from messages left join dislike_reacted using(mid)" \
                " group by mid, text, mtime, messages.uid, cid, isdeleted, rid order by mtime)) " \
                "select mid, like_messages.text, like_messages.mtime, pseudonym, like_messages.uid, " \
                "like_messages.cid, like_messages.isdeleted, like_messages.rid, likes, dislikes" \
                " from like_messages inner join dislike_messages using(mid) inner join users on " \
                "users.uid = like_messages.uid where like_messages.cid = %s and like_messages.isdeleted = 'f'" \
                " and STRPOS(lower(like_messages.text), lower(%s)) > 0 order by mtime desc"
        cursor.execute(query, (cID, search))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ========================= Methods Independent On Time ======================= #
    # ============== Methods For Get Messages ============ #
    def getAllMessages(self):
        cursor = self.conn.cursor()
        query = "with like_messages as " \
	    "(with like_reacted as (select * from reacted where vote = 1)" \
	    "(select mid, text, mtime, messages.uid, cid, isdeleted, rid, count(vote) as likes" \
	    " from messages left join like_reacted using(mid)" \
	    " group by mid, text, mtime, messages.uid, cid, isdeleted, rid" \
	    " order by mtime)), dislike_messages as " \
	    " (with dislike_reacted as (select * from reacted where vote = -1)" \
	    " (select mid, text, mtime, messages.uid, cid, isdeleted, rid, count(vote) as dislikes" \
	    " from messages left join dislike_reacted using(mid)" \
	    " group by mid, text, mtime, messages.uid, cid, isdeleted, rid order by mtime)) " \
        "select mid, like_messages.text, like_messages.mtime, pseudonym, like_messages.uid, " \
        "like_messages.cid, like_messages.isdeleted, like_messages.rid, likes, dislikes" \
        " from like_messages inner join dislike_messages using(mid) inner join users on " \
        "users.uid = like_messages.uid order by mtime desc"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result


    def getAllReplyMessages(self):
        cursor = self.conn.cursor()
        query = "select * from messages where rid is not NULL;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllRepliedMessages(self):
        cursor = self.conn.cursor()
        query = "select * from messages where mid in (Select rid from messages where rid is not NULL);"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMessagesWithMedia(self):
        cursor = self.conn.cursor()
        query = "select * from messages where mid in (Select mid from medias);"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMessagesWithReactions(self):
        cursor = self.conn.cursor()
        query = "select * from messages where mid in (Select mid from reacted);"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMessagesWithTopics(self):
        cursor = self.conn.cursor()
        query = "select * from messages where mid in (Select mid from topics);"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllActiveMessages(self, isDeleted):
        cursor = self.conn.cursor()
        query = "Select * from Messages where isDeleted = %s;"
        cursor.execute(query, (isDeleted, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ============ Get Messages by chat type ================== #
    def getAllMessagesInChatType(self, isGroupChat):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, " \
                "rid from chats inner join messages using(cid) where isgroupchat = %s;"
        cursor.execute(query, (isGroupChat, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllActiveMessagesInChatType(self, isGroupChat, isDeleted):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, " \
                "rid from chats inner join messages using(cid) where isdeleted = %s" \
                " and isgroupchat = %se;"
        cursor.execute(query, (isDeleted, isGroupChat, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllReplyMessagesInChatType(self, isGroupChat):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, " \
                "rid from chats inner join messages using(cid) where isGroupChat = %s " \
                "and rid is not NULL;"
        cursor.execute(query, (isGroupChat,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllRepliedMessagesInChatType(self, isGroupChat):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, rid " \
                "from chats inner join messages using(cid) where isGroupChat = %s " \
                "and mid in (select rid from messages);"
        cursor.execute(query, (isGroupChat,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMessagesWithMediaInChatType(self, isGroupChat):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, rid" \
                " from messages inner join chats using(cid) where mid in (Select mid from medias)" \
                "and isGroupChat = %s;"
        cursor.execute(query, (isGroupChat, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMessagesWithReactionsInChatType(self, isGroupChat):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, rid" \
                " from messages inner join chats using(cid) where mid in (Select mid from reacted)" \
                "and isGroupChat = %s;"
        cursor.execute(query, (isGroupChat,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMessagesWithTopicsInChatType(self, isGroupChat):
        cursor = self.conn.cursor()
        query = "select mid, text, mtime, messages.uid, cid, isdeleted, rid" \
                " from messages inner join chats using(cid) where mid in (Select mid from topics)" \
                "and isGroupChat = %s;"
        cursor.execute(query, (isGroupChat,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ============== Get Messages in chats ================== #
    def getAllChatMessages(self, cID):
        cursor = self.conn.cursor()
        query = "with like_messages as " \
                "(with like_reacted as (select * from reacted where vote = 1)" \
                "(select mid, text, mtime, messages.uid, cid, isdeleted, rid, count(vote) as likes" \
                " from messages left join like_reacted using(mid)" \
                " group by mid, text, mtime, messages.uid, cid, isdeleted, rid" \
                " order by mtime)), dislike_messages as " \
                " (with dislike_reacted as (select * from reacted where vote = -1)" \
                " (select mid, text, mtime, messages.uid, cid, isdeleted, rid, count(vote) as dislikes" \
                " from messages left join dislike_reacted using(mid)" \
                " group by mid, text, mtime, messages.uid, cid, isdeleted, rid order by mtime)) " \
                "select mid, like_messages.text, like_messages.mtime, pseudonym, like_messages.uid, " \
                "like_messages.cid, like_messages.isdeleted, like_messages.rid, likes, dislikes" \
                " from like_messages inner join dislike_messages using(mid) inner join users on " \
                "users.uid = like_messages.uid where like_messages.cid = %s and like_messages.isdeleted = 'f'" \
                " order by mtime desc"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatActiveMessages(self, cID, isDeleted):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "isdeleted = %s and cid = %s;"
        cursor.execute(query, (isDeleted, cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatReplyMessages(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "rid is not NULL and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatRepliedMessages(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from messages) and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatMessagesWithMedia(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select mid from media) and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatMessagesWithTopic(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select mid from topics) and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatMessagesWithReactions(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select mid from reacted) and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatMessagesWithLikes(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select mid from reacted where vote = 1) and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatMessagesWithDisikes(self,cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select mid from reacted where vote = -1) and cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ========= Get Messages By User ================== #
    def getAllUserMessages(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserActiveMessages(self, uID, isDeleted):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "isdeleted = %s and uid = %s;"
        cursor.execute(query, (isDeleted, uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserReplyMessages(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "rid is not NULL and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserRepliedMessages(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from messages) and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithMedia(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from medias) and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithTopic(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from topics) and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithReactions(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from reacted) and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithLikes(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from reacted where vote = 1) and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithDisikes(self, uID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from reacted where vote = -1) and uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ========= Get Messages by Chat and User ========== #
    def getAllUserMessagesInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where uid = %s and cid = %s;"
        cursor.execute(query, (uID, cID))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserActiveMessagesInChat(self, uID, isDeleted, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "isdeleted = %s and uid = %s and cid = %s;"
        cursor.execute(query, (isDeleted, uID, cID))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserReplyMessagesInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "rid is not NULL and uid = %s and cid = %s;"
        cursor.execute(query, (uID, cID))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserRepliedMessagesInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from messages) and uid = %s and cid = %s;"
        cursor.execute(query, (uID, cID))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithMediaInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from medias) and uid = %s and cid = %s;"
        cursor.execute(query, (uID, cID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithTopicInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from topics) and uid = %s and cid = %s;"
        cursor.execute(query, (uID,cID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithReactionsInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from reacted) and uid = %s and cid = %s;"
        cursor.execute(query, (uID, cID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithLikesInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from reacted where vote = 1) and uid = %s and cid = %s;"
        cursor.execute(query, (uID,cID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUserMessagesWithDisikesInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select * from messages where " \
                "mid in (select rid from reacted where vote = -1) and uid = %s;"
        cursor.execute(query, (uID,cID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result
    # ===================== Get Topics ========================= #

    def getAllTopics(self):
        cursor = self.conn.cursor()
        query = "select * from topics;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllTopicsInMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select * from topics where mid = %s;"
        cursor.execute(query, (mID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllTopicsInChat(self, cID):
        cursor = self.conn.cursor()
        query = "select tid, hashtag, mid, ttime from topics natural inner join messages where cid = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllTopicsByUser(self, uID):
        cursor = self.conn.cursor()
        query = "select tid, hashtag, mid, ttime from topics natural inner join messages where uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllTopicsByUserInChat(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select hashtag, mid from topics natural inner join messages where uid = %s and cid = %s;"
        cursor.execute(query, (uID,cID))
        result = []
        for row in cursor:
            result.append(row)
        return result


    # =================================== Get Reactions =================================== #

    def getAllReactions(self):
        #WORKSSSSSSSSSSSSSSSSSS
        cursor = self.conn.cursor()
        query = "select * from reacted;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllLikes(self):
        #WORKSSSSSS
        cursor = self.conn.cursor()
        query = "select * from reacted where vote = 1;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllDislikes(self):
        #WORKSSSSSSSSSSS
        cursor = self.conn.cursor()
        query = "select * from reacted where vote = -1;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllReactionsInMessage(self, mID):
        #WORKSSSSSSSSS
        cursor = self.conn.cursor()
        query = "select * from reacted where mid = %s;"
        cursor.execute(query, (mID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllLikesInMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select * from reacted where mid = %s and vote = 1;"
        cursor.execute(query, (mID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllDislikesInMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select * from reacted where mid = %s and vote = -1;"
        cursor.execute(query, (mID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Returns the list of reactions of the user with ID uID
    def getAllReactionsByUser(self, uID):
        #WORKSSSSSSSSSSSSSS
        cursor = self.conn.cursor()
        query = "select * from reacted where uid = %s;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllLikesByUser(self, uID):
        cursor = self.conn.cursor()
        query = "select * from reacted where uid = %s and vote = 1;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllDislikesByUser(self, uID):
        cursor = self.conn.cursor()
        query = "select * from reacted where uid = %s and vote = -1;"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllReactionsInChat(self, cID):
        cursor = self.conn.cursor()
        query = "select uid, mid, rtime, vote from reacted inner join messages using(mid)" \
                " where chat = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllLikesInChat(self, cID):
        cursor = self.conn.cursor()
        query = "select uid, mid, rtime, vote from reacted inner join messages using(mid)" \
                " where chat = %s and vote = 1;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllDislikesInChat(self, cID):
        cursor = self.conn.cursor()
        query = "select uid, mid, rtime, vote from reacted inner join messages using(mid)" \
                " where chat = %s and vote = -1;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCountReactionsInMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select count(*) from reacted" \
                " where mid = %s;"
        cursor.execute(query, (mID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCountLikesInMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select count(*) from reacted" \
                " where mid = %s and vote = 1;"
        cursor.execute(query, (mID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCountDislikesInMessage(self, mID):
        cursor = self.conn.cursor()
        query = "select count(*) from reacted" \
                " where mid = %s and vote = -1;"
        cursor.execute(query, (mID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # =================================== Get Media ============================= #
    def getAllMedia(self):
        cursor = self.conn.cursor()
        query = "select * from medias;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMessageMedia(self, mID):
        cursor = self.conn.cursor()
        query = "select * from medias where mid = %s;"
        cursor.execute(query, (mID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMediaInChat(self, cID):
        cursor = self.conn.cursor()
        query = "select mid, isvideo, location from medias natural inner join messages where cid = %s"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMediaByUser(self, uID):
        cursor = self.conn.cursor()
        query = "select mid, isvideo, location from medias natural inner join messages where uid = %s"
        cursor.execute(query, (uID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllMediaInChatByUser(self, uID, cID):
        cursor = self.conn.cursor()
        query = "select mid, isvideo, location from medias natural inner join messages " \
                "where uid = %s and cid = %s"
        cursor.execute(query, (uID, cID, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ~~~~~~~~~~~~~~~~~ Dashboard ~~~~~~~~~~~~~~~~~~~~~~~~~~~~``` #

    def getTopTopics(self):
        cursor = self.conn.cursor()
        query = "select hashtag, count(*) as Usage from topics group by hashtag order by Usage desc;"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
            print(row)
        return result

    def getMessagesPerDay(self, btime, atime):
        cursor = self.conn.cursor()
        query = "select count(*) from messages where mtime > %s and mtime < %s;"
        cursor.execute(query, (btime, atime))
        result = []
        for row in cursor:
            result.append(row)
        return result[0]

    def getRepliesPerDay(self, btime, atime):
        cursor = self.conn.cursor()
        query = "select count(*) from messages where rid is not NULL and mtime > %s and mtime < %s;"
        cursor.execute(query, (btime, atime))
        result = []
        for row in cursor:
            result.append(row)
        return result[0]

    def getLikesPerDay(self, btime, atime):
        cursor = self.conn.cursor()
        query = "select count(*) from reacted" \
                " where vote = 1 and rtime > %s and rtime < %s;"
        cursor.execute(query, (btime, atime))
        result = []
        for row in cursor:
            result.append(row)
        return result[0]

    def getDislikesPerDay(self, btime, atime):
        cursor = self.conn.cursor()
        query = "select count(*) from reacted" \
                " where vote = -1 and rtime > %s and rtime < %s;"
        cursor.execute(query, (btime, atime))
        result = []
        for row in cursor:
            result.append(row)
        return result[0]





