import React from 'react'
import axios from 'axios'
declare const window: any;
class Component extends React.Component {

    state = {
        isLoading: true,
        shortenedData: []
    }

    componentDidMount() {
        
        axios.get(`${window.REACT_APP_BACKEND_URL}/`).then(response => {
            this.setState({
                isLoading: false,
                shortenedData: response.data
            })
        }).catch(error => console.error(error))
    }

    render(){
        if (this.state.isLoading) return <div className="loader"></div>

        return <div id="page_products"> 
            {
                this.state.shortenedData.map((url, i) => {
                    return <div>
                    url
                    </div>
                })
            }
        </div>
    }
}

export default Component