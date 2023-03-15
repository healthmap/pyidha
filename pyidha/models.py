from datetime import datetime


def write_repo_data(list_of_model_objects, session):
    """Given a list of model objects, write them to the database.

    This function is to be used inside an active Session context.

    Parameters
    __________
    list_of_model_objects : list of Model
        A list of SQLAlchemy Model objects.
    session : Session
        a SQLAlachemy Session object

    Returns
    _______
    None

    Examples
    ________
    >>> with Session() as session:
    ...     write_repo_data(list_of_model_objects, session)

    """
    try:
        for item in list_of_model_objects:
            item.last_update = datetime.now()  # last time the repo was updated
            session.add(item)
            session.commit()
            print(f"successfully committed {item}")

    except Exception as e:
        print("write_repo_data", e)
