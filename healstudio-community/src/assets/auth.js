import axios from "axios"

const BASE_URL = "http://localhost:8000"

export const get_user_details = async (user_id, uuid) => {
    const url = `${BASE_URL}/user/${user_id}`
    const result = await axios.get(url, {params: {
        uid: uuid
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

