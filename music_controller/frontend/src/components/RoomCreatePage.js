import React, { Component } from "react";
import {
    Button,
    Collapse,
    Typography,
    Grid,
    TextField,
    FormHelperText,
    FormControl,
    Radio,
    RadioGroup,
    FormControlLabel,
} from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { Link } from "react-router-dom";

export default class RoomCreatePage extends Component {
    static defaultProps = {
        guestCanPause: false,
        votesToSkip: 2,
        update: false,
        roomCode: null,
        updateCallback: () => {},
    };

    constructor(props) {
        super(props);
        this.state = {
            guestCanPause: this.props.guestCanPause,
            votesToSkip: this.props.votesToSkip,
            successMsg: "",
            errorMsg: "",
        };
    }

    handleVotesToSkipChange = (e) => {
        this.setState({
            votesToSkip: e.target.value,
        });
    };

    handleGuestCanPauseChange = (e) => {
        this.setState({
            guestCanPause: e.target.value === "true" ? true : false,
        });
    };

    handleRoomButtonClicked = () => {
        if (!this.props.update) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    votes_to_skip: this.state.votesToSkip,
                    guest_can_pause: this.state.guestCanPause,
                }),
            };
            fetch("/api/create-room", requestOptions)
                .then((response) => response.json())
                .then((data) => this.props.history.push("/room/" + data.code));
        } else {
            const requestOptions = {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    votes_to_skip: this.state.votesToSkip,
                    guest_can_pause: this.state.guestCanPause,
                    room_code: this.props.roomCode,
                }),
            };
            fetch("/api/update-room", requestOptions).then((response) => {
                if (response.ok) {
                    this.setState({
                        successMsg: "Room settings updated successfully!",
                    });
                } else {
                    response.json().then((data) => {
                        this.setState({
                            errorMsg: data[Object.keys(data)[0]],
                        });
                    });
                }
                this.props.updateCallback();
            });
        }
    };

    render() {
        const title = this.props.update ? "Update Room" : "Create a Room";
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Collapse in={this.state.errorMsg || this.state.successMsg}>
                        {this.state.successMsg ? (
                            <Alert
                                severity="success"
                                onClose={() => {
                                    this.setState({ successMsg: "" });
                                }}
                            >
                                {this.state.successMsg}
                            </Alert>
                        ) : (
                            <Alert
                                severity="error"
                                onClose={() => {
                                    this.setState({ errorMsg: "" });
                                }}
                            >
                                {this.state.errorMsg}
                            </Alert>
                        )}
                        {this.state.errorMsg}
                    </Collapse>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography component="h4" variant="h4">
                        {title}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl component="fieldset">
                        <FormHelperText>
                            <div align="center">
                                Guest Control of Playback State
                            </div>
                        </FormHelperText>
                        <RadioGroup
                            row
                            defaultValue={this.state.guestCanPause.toString()}
                            onChange={this.handleGuestCanPauseChange}
                        >
                            <FormControlLabel
                                value="true"
                                control={<Radio color="primary" />}
                                label="Play/Pause"
                                labelPlacement="bottom"
                            />
                            <FormControlLabel
                                value="false"
                                control={<Radio color="secondary" />}
                                label="No Control"
                                labelPlacement="bottom"
                            />
                        </RadioGroup>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <FormControl>
                        <TextField
                            required="true"
                            type="number"
                            defaultValue={this.state.votesToSkip}
                            inputProps={{
                                min: 1,
                                style: {
                                    textAlign: "center",
                                },
                            }}
                            onChange={this.handleVotesToSkipChange}
                        />
                        <FormHelperText>
                            <div align="center">
                                Votes Required to Skip Song
                            </div>
                        </FormHelperText>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button
                        color="primary"
                        variant="contained"
                        onClick={this.handleRoomButtonClicked}
                    >
                        {title}
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button
                        color="secondary"
                        variant="contained"
                        to="/"
                        component={Link}
                    >
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    }
}
