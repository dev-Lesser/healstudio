import axios from "axios"

const BASE_URL = "http://localhost:8000"

export const get_boards = async (skip, limit, user) => {
    const url = `${BASE_URL}/boards`
    const result = await axios.get(url, {params: {
        skip: skip,
        limit: limit,
        user: user
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}
export const get_boards_reload = async (skip, limit, user, reload) => {
    const url = `${BASE_URL}/boards`
    const result = await axios.get(url, {params: {
        skip: skip,
        limit: limit,
        user: user,
        reload: reload
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

export const get_board = async (id, user, login_user, skip, limit) => {
    const url = `${BASE_URL}/board/${id}`
    const result = await axios.get(url, {params: {
        user: user,
        login_user: login_user,
        skip: skip,
        limit: limit
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

export const create_board = async (user_id, uid, title, contents) => {
    const body = { user_id, uid, title, contents }
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'post',
        url: `${BASE_URL}/board`,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 201) {
        return true
    }
    return false
}

export const edit_board = async (user_id, uid, id, title, contents) => {
    const body = { user_id, uid, id, title, contents }
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'patch',
        url: `${BASE_URL}/board`,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 204) {
        return true
    }
    return false
}


export const delete_board = async (user_id, uid, id, title) => {
    const result = await axios({
        method: 'delete',
        url: `${BASE_URL}/board`,
        headers: {
            'Content-Type': 'application/json'
        },
        params: {
            user_id: user_id,
            uid: uid,
            id: id,
            title: title,
        }
    })
    if (result.status == 200) {
        return true
    }
    return false
}

export const create_reply = async (user_id, uid, id, contents) => {
    const body = { user_id, uid, id, contents }
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'post',
        url: `${BASE_URL}/reply`,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 201) {
        return [true, result.data]
    }
    return false
}
export const delete_reply = async (user_id, uid, id) => {
    const result = await axios({
        method: 'delete',
        url: `${BASE_URL}/reply`,
        headers: {
            'Content-Type': 'application/json'
        },
        params: {
            user_id: user_id,
            uid: uid,
            id: id,
        }
    })
    if (result.status == 200) {
        return true
    }
    return false
}

export const handle_favorite = async (user_id, uid, id, creater_id) => {
    const body = { user_id, uid, creater_id }
    const url = `${BASE_URL}/board/${id}/favorite`
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'patch',
        url: url,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 200) {
        return [true, result.data]
    }
    return false
}