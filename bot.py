import redis
import connect
from redis_lru import RedisLRU
from abc import ABC, abstractmethod
from models import Quotes, Authors, Tag

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


class DataProvider(ABC):
    def __init__(self) -> None:
        ...

    @abstractmethod
    def query_author_by_name(self, name: str):
        ...

    @abstractmethod
    def query_quotes_by_author(self, author) -> list[str]:
        ...

    @abstractmethod
    def query_quotes_by_tags(self, tags: list[str]) -> list[str]:
        ...


class MongoDataProvider(DataProvider):
    def __init__(self) -> None:
        ...

    def query_author_by_name(self, name: str) -> Authors:
        author = Authors.objects(fullname__istartswith=name).first()
        return author

    def query_quotes_by_author(self, author: Authors) -> list[str]:
        try:
            quotes = Quotes.objects(author=author.id)
            return self.__format_quotes(quotes)
        except AttributeError:
            return None

    def query_quotes_by_tags(self, tags: list[str]) -> list[str]:
        quotes = Quotes.objects(tags__name__in=tags)
        return self.__format_quotes(quotes)
    
    def __format_quotes(self, quotes: Quotes) -> list[str]:
        result = []
        for quote in quotes:
            result.append(f"{quote.quote}")
        return result


class DataManager():
    def __init__(self, data_provider: DataProvider) -> None:
        self.__data_provider: DataProvider = data_provider

    @cache
    def query_by_author(self, name: str) -> list[str]:
        author = self.__data_provider.query_author_by_name(name)
        if author:
            result = self.__data_provider.query_quotes_by_author(author)
        else: 
            result = [f"Author with name '{name.title()}' not found"]        
        return result or ["No results found"]

    @cache
    def query_by_tags(self, tags: list[str]) -> str:
        result = self.__data_provider.query_quotes_by_tags(tags)
        return result or ["No results found"]


class CommandManager:
    def __init__(self, data_manager: DataManager) -> None:
        self._exit_commands = {"good bye", "close", "exit", "stop", "g"}
        self._commands = {"name": self.get_quotes_by_author, "tag": self.get_quotes_by_tags, "tags": self.get_quotes_by_tags}
        self._data_manager = data_manager

    def is_exit(self, user_input) -> bool:
        return user_input in self._exit_commands

    def handle_command(self, user_input: str) -> str:
        args = user_input.lower().split(":")
        try:
            return self._commands[args[0]](args[1].strip())
        except KeyError:
            return "Unknown command"
        except IndexError:
            return "Wrong command format"

    def get_quotes_by_author(self, name: str) -> str:
        return self._data_manager.query_by_author(name)

    def get_quotes_by_tags(self, tags: str) -> str:
        tag_list = tags.split(",")
        return self._data_manager.query_by_tags(tag_list)


def format_output(output) -> str:
    if isinstance(output, str):
        return output
    return "\n".join(output)


def get_help() -> str:
    return """
    Supported commands:
    name: [author name] - prints quotes by author name
    tag:[tag] - prints quotes by a tag
    tags:[tag-1],[tag-2],...,[tag-n] - prints quotes by a tags
    For exit enter any of exit-commands:
    good bye | close | exit | stop
"""


def main():
    manager = CommandManager(DataManager(MongoDataProvider()))
    print(get_help())
    while True:
        user_input = input(">>> ")

        if manager.is_exit(user_input):
                print("Good bye!")
                break
        
        print(format_output(manager.handle_command(user_input)))


if __name__ == '__main__':
    main()
