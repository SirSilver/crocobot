import random
import sqlite3


class Game:

    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.words_file = 'categories/words.txt'
        self.celebrities_file = 'categories/celebrities.txt'
        self.movies_file = 'categories/movies.txt'

    def create_tables(self):
        with self.connection:
            self.cursor.executescript("""
                    CREATE TABLE IF NOT EXISTS players(
                        id INTEGER NOT NULL UNIQUE PRIMARY KEY,
                        name TEXT NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS chats(
                        id INTEGER NOT NULL UNIQUE PRIMARY KEY,
                        name TEXT NOT NULL,
                        categories TEXT DEFAULT "movies celebrities general",
                        speaker INTEGER,
                        correct_word TEXT,
                        in_play INTEGER NOT NULL DEFAULT 0,
                        FOREIGN KEY (speaker) REFERENCES players(id)
                    );

                    CREATE TABLE IF NOT EXISTS scores(
                        chat_id INTEGER NOT NULL,
                        player_id INTEGER NOT NULL,
                        score INTEGER NOT NULL DEFAULT 0,
                        FOREIGN KEY (chat_id) REFERENCES chats(id),
                        FOREIGN KEY (player_id) REFERENCES players(id))""")

    def player_exists(self, player_id):
        if self.get_player_name(player_id) is None:
            return False
        return True

    def chat_exists(self, chat_id):
        if self.get_chat_name(chat_id) is None:
            return False
        return True

    def score_exists(self, chat_id, player_id):
        if self.get_score(chat_id, player_id) is None:
            return False
        return True

    def add_player(self, player_id, player_name):
        with self.connection:
            self.cursor.execute('INSERT INTO players (id, name) VALUES (?,?)', (player_id, player_name))

    def add_chat(self, chat_id, chat_name):
        with self.connection:
            self.cursor.execute('INSERT INTO chats (id, name) VALUES (?,?)', (chat_id, chat_name))

    def add_score(self, chat_id, player_id):
        with self.connection:
            self.cursor.execute('INSERT INTO scores (chat_id, player_id) VALUES (?,?)', (chat_id, player_id))

    def get_player_name(self, player_id):
        result = self.cursor.execute('SELECT name FROM players WHERE id = ?', (player_id,)).fetchone()
        if result is None:
            return None
        return result[0]

    def get_chat_name(self, chat_id):
        result = self.cursor.execute('SELECT name FROM chats WHERE id = ?', (chat_id,)).fetchone()
        if result is None:
            return None
        return result[0]

    def get_chat_categories(self, chat_id):
        result = self.cursor.execute('SELECT categories FROM chats WHERE id = ?', [chat_id]).fetchone()
        if result is None:
            return None
        return result[0].split()

    def edit_chat_category(self, chat_id, category, action):
        categories = self.get_chat_categories(chat_id)
        if action == 'add':
            categories.append(category)
        else:
            categories.remove(category)
        with self.connection:
            self.cursor.execute('UPDATE chats SET categories = ? WHERE id = ?', (' '.join(categories), chat_id))

    def get_speaker_id(self, chat_id):
        result = self.cursor.execute('SELECT speaker FROM chats WHERE id = ?', (chat_id,)).fetchone()
        if result is None:
            return None
        return result[0]

    def get_speaker_name(self, chat_id):
        result = self.get_player_name(player_id=self.get_speaker_id(chat_id))
        return result

    def set_speaker(self, chat_id, speaker_id):
        with self.connection:
            self.cursor.execute('UPDATE chats SET speaker = ? WHERE id = ?', (speaker_id, chat_id))

    def get_correct_word(self, chat_id):
        result = self.cursor.execute('SELECT correct_word FROM chats WHERE id = ?', (chat_id,)).fetchone()
        if result is None:
            return None
        return result[0]

    def set_correct_word(self, chat_id):
        WORDS = []
        categories = self.get_chat_categories(chat_id=chat_id)
        if 'celebrities' in categories:
            WORDS += open(self.celebrities_file).read().splitlines()
        if 'movies' in categories:
            WORDS += open(self.movies_file).read().splitlines()
        if 'general' in categories:
            WORDS += open(self.words_file).read().splitlines()
        correct_word = random.choice(WORDS)
        with self.connection:
            self.cursor.execute('UPDATE chats SET correct_word = ? WHERE id = ?', (correct_word, chat_id))

    def get_score(self, chat_id, player_id):
        result = self.cursor.execute('SELECT score FROM scores WHERE chat_id = ? AND player_id = ?', (chat_id, player_id)).fetchone()
        if result is None:
            return None
        return result[0]

    def get_score_table(self, chat_id):
        result = []
        players = self.cursor.execute('SELECT * FROM scores WHERE chat_id = ? ORDER BY score DESC', (chat_id,)).fetchmany(10)
        for player in players:
            player_name = self.get_player_name(player[1])
            player_score = player[2]
            result.append([player_name, player_score])
        return result

    def increase_score(self, chat_id, player_id):
        with self.connection:
            self.cursor.execute('UPDATE scores SET score = score + 1 WHERE chat_id = ? AND player_id = ?', (chat_id, player_id))

    def in_play(self, chat_id):
        if self.cursor.execute('SELECT in_play FROM chats WHERE id = ?', (chat_id,)).fetchone()[0] == 1:
            return True
        return False

    def change_state(self, chat_id, state):
        with self.connection:
            self.cursor.execute('UPDATE chats SET in_play = ? WHERE id = ?', (state, chat_id))
