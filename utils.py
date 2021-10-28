from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///doc_tracker.db")
Session = sessionmaker(bind=engine)


def get_session():
    return Session()

# for more examples google sqllachemy + SQL OPERATION
# session = get_session()
# session.query(NasaTabela).all()
# session.query(NasaTabela).filter(NasaTabela.ime=='primer').all()
# session.query(NasaTabela).filter_by(ime='primer').all()

# all - vraca listu, prazna ako nema
# one - vrati jedan, ako nema raise-uje NoResultsFound, raiseuje ako ima vise
# one_or_none - vrati jedno ili None, raisuje exc ako ima vise
# first - prvi ili None

# from db_models import NasaTabela
#
# nt = NasaTabela(ime="Milos", godina=27)
# session.add(nt)
# session.commit()
# session.close()