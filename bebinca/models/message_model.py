from datetime import datetime

from bebinca.models.base import BaseModel


class MessageModel(BaseModel):

    async def add_message(self, chat_id, trace_id, sender):
        sql_str = '''
            INSERT INTO messages (ChatID, TraceID, Sender) 
            VALUES (%s, %s, %s)
        '''
        await self.conn()
        await self.execute(sql_str, (chat_id, trace_id, sender))
        await self.commit()
        lastrowid = self.cursor.lastrowid
        await self.close()
        return lastrowid
