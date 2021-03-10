from datetime import datetime


def test_index(client):
    from jeockovanibezpecne.models import Submit, Vaccine, Dead, Case
    from jeockovanibezpecne.update import update

    t = datetime.now()
    s_t = Submit.query.order_by(Submit.date_for.desc()).first().timestamp
    v_t = Vaccine.query.order_by(Vaccine.date_for.desc()).first().timestamp
    d_t = Dead.query.order_by(Dead.date_for.desc()).first().timestamp
    c_t = Case.query.order_by(Case.date_for.desc()).first().timestamp

    update(t)

    assert len(Submit.query.all()) > 0
    ss = Submit.query.order_by(Submit.date_for.desc()).first()
    assert ss.timestamp != s_t

    assert len(Vaccine.query.all()) > 0
    ss = Vaccine.query.order_by(Vaccine.date_for.desc()).first()
    assert ss.timestamp != v_t

    assert len(Dead.query.all()) > 0
    ss = Dead.query.order_by(Dead.date_for.desc()).first()
    assert ss.timestamp != d_t

    assert len(Case.query.all()) > 0
    ss = Case.query.order_by(Case.date_for.desc()).first()
    assert ss.timestamp != c_t
