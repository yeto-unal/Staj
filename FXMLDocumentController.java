/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package banking_application;

import java.net.URL;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javax.swing.JOptionPane;

/**
 *
 * @author Yetkin
 */
public class FXMLDocumentController implements Initializable {
    
    @FXML
    private TextField username;

    @FXML
    private PasswordField passwd;

    @FXML
    private Button bttn;

    @FXML
    private Label lblErrors;
    
    Connection con;
    PreparedStatement pst;
    ResultSet rs;

    @FXML
    void login(ActionEvent event) {
        String uname = username.getText();
        String password = passwd.getText().toString();
        
        if(uname.equals("") && password.equals("")){
            JOptionPane.showMessageDialog(null, "Kullanıcı adı veya şifre kısmı boş bırakılamaz.");
        }
        else{
            try{
                Class.forName("com.mysql.jdbc.Driver");
                con = DriverManager.getConnection("jdbc:mysql://localhost:3306/banka", "root", "p3mb3pant3r");
                pst = con.prepareStatement("SELECT * FROM login_info WHERE Username=? and Password=?");
                
                pst.setString(1, uname);
                pst.setString(2, password);
                
                rs = pst.executeQuery();
                
                if(rs.next()){
                    JOptionPane.showMessageDialog(null, "Giriş Başarılı");
                }
                else{
                    JOptionPane.showMessageDialog(null, "Giriş Başarısız");
                    username.setText("");
                    passwd.setText("");
                    username.requestFocus();
                    
                }
            }catch(ClassNotFoundException ex){
                Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
            }catch(SQLException ex){
                Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        // TODO
    }    
    
}
