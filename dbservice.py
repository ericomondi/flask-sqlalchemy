def register_user(full_name, email, password):
    new_user = Users(full_name=full_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()