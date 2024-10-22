import asyncio
from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from database import init_db, AsyncSessionFactory, Course  # type: ignore
from sqlalchemy.orm import make_transient, Mapped


async def main():
    # Инициализируем базу данных
    await init_db()

    class HasIs(Protocol):
        id: Mapped[int]

    # Detach object function
    def detach_object(obj: HasIs) -> None:
        make_transient(obj)
        obj.id = None

    # Clone course function
    async def clone_course(session: AsyncSession, course_id: int) -> Course | None:
        course = await session.get(Course, course_id)
        if course:
            detach_object(course)
            course.id = None
            session.add(course)
            await session.commit()
            return course
        return None

    # Создадим сессию
    async with AsyncSessionFactory() as session:
        # Добавим новый курс
        course = Course(name="Python 101", description="Basic Python course")
        session.add(course)
        await session.commit()
        print(f"Course created with ID: {course.id}")

        # Клонируем курс
        cloned_course = await clone_course(session, course.id)
        if cloned_course:
            print(f"Cloned course with new ID: {cloned_course.id}")
        else:
            print("Course not found!")


if __name__ == "__main__":
    asyncio.run(main())
