def select(name):
    if name == 'potapov':
        from app.modules.teachers.potapov import checker, task1_loader, task2_loader
        return checker, task1_loader, task2_loader
    elif name == 'tumakova':
        from app.modules.teachers.tumakova import checker, task1_loader, task2_loader
        return checker, task1_loader, task2_loader