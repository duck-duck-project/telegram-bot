from models import ManasId

__all__ = ('generate_manas_id_number',)


def generate_manas_id_number(manas_id: ManasId) -> str:
    abbreviated_full_name = (
        f'{manas_id.first_name[0]}'
        f'{manas_id.last_name[0]}'
    ).upper()
    abbreviated_department_name = ''.join(
        name[0] for name in
        manas_id.department.name.upper().split(' ')[1:]
    )
    return (
        f'{manas_id.gender}'
        f'{abbreviated_full_name}'
        f'{manas_id.born_at:%d%m%y}'
        f'{abbreviated_department_name}'
    )
