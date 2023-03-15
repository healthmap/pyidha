from datetime import datetime
from sqlalchemy.orm import Session


def write_repo_data(list_of_model_objects):
    """Given a list of model objects, write them to the database.

    Parameters
    __________
    list_of_model_objects : list of obj
        A list of model objects.

    Returns
    _______
    None

    """
    with Session() as session:
        try:
            for item in list_of_model_objects:
                item.last_update = datetime.now()  # last time the repo was updated
                session.add(item)
                session.commit()
                print(f"successfully committed {item}")

        except Exception as e:
            print("write_repo_data", e)
