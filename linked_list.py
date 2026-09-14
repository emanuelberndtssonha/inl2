from typing import Optional, List
from models import Node, Session
from datetime import date

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def insert_sorted(self, session: Session) -> None:
        new_node = Node(session)
        
        if not self.head or session.session_date < self.head.data.session_date:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while current.next and current.next.data.session_date <= session.session_date:
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def get_sessions_by_date(self, target_date: date) -> List[Session]:
        sessions = []
        current = self.head
        while current:
            if current.data.session_date == target_date:
                sessions.append(current.data)
            current = current.next
        return sessions

    def delete_by_index(self, index: int) -> bool:
        if not self.head or index < 0:
            return False

        if index == 0:
            self.head = self.head.next
            return True

        current = self.head
        count = 0
        while current.next and count < index - 1:
            current = current.next
            count += 1

        if current.next:
            current.next = current.next.next
            return True
        return False

    def to_list(self) -> List[Session]:
        sessions = []
        current = self.head
        while current:
            sessions.append(current.data)
            current = current.next
        return sessions